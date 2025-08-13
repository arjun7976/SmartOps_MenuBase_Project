"""
Face Swap Module

This module provides functionality to swap faces between two images using OpenCV and dlib.
It's designed to be used as part of the Python Automation section.
"""

import os
import tempfile
import numpy as np
import cv2
import dlib
import streamlit as st
from typing import Tuple, List

def check_dependencies() -> Tuple[bool, str]:
    """Check if all required dependencies are installed.
    
    Returns:
        Tuple[bool, str]: (success, message) indicating if dependencies are met
    """
    try:
        import cv2
        import dlib
        import numpy as np
        return True, "All dependencies are installed."
    except ImportError as e:
        missing = []
        if 'cv2' in str(e):
            missing.append("opencv-python")
        if 'dlib' in str(e):
            missing.append("dlib")
        if 'numpy' in str(e):
            missing.append("numpy")
        return False, f"Missing dependencies: {', '.join(missing)}. Install with: pip install {' '.join(missing)}"

def load_and_prepare_image(uploaded_file) -> Tuple[np.ndarray, str]:
    """Load and prepare an uploaded image file.
    
    Args:
        uploaded_file: File object from Streamlit file_uploader
        
    Returns:
        Tuple containing (image array, temp_file_path)
    """
    if uploaded_file is None:
        return None, ""
    
    try:
        # Read the file bytes
        file_bytes = np.frombuffer(uploaded_file.getvalue(), np.uint8)
        
        # Read the image using OpenCV
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if image is None:
            # Try alternative approach if the first one fails
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(uploaded_file.getvalue())
            temp_file.close()
            
            image = cv2.imread(temp_file.name)
            os.unlink(temp_file.name)  # Clean up the temp file
            
            if image is None:
                raise ValueError("Could not decode the image. Please upload a valid image file.")
        
        # Convert from BGR to RGB for dlib
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Create a temporary file for reference
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        cv2.imwrite(temp_file.name, image)  # Save as BGR for OpenCV
        
        return image_rgb, temp_file.name
        
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None, ""

def detect_landmarks(image: np.ndarray) -> Tuple[dlib.rectangle, dlib.full_object_detection]:
    """Detect face landmarks using dlib.
    
    Args:
        image: Input image in BGR format
        
    Returns:
        Tuple containing (face_rectangle, landmarks)
    """
    if image is None:
        raise ValueError("Input image is None")
        
    # Ensure image is in the correct format (numpy array)
    if not isinstance(image, np.ndarray):
        raise ValueError("Input must be a numpy array")
        
    # Convert to grayscale for detection (dlib requires uint8)
    if image.dtype != np.uint8:
        if image.max() <= 1.0:  # If values are in 0-1 range
            image = (image * 255).astype(np.uint8)
        else:
            image = image.astype(np.uint8)
    
    # Convert to grayscale if it's a color image
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:
        gray = image  # Already grayscale
    else:
        raise ValueError("Unsupported image format. Expected BGR or grayscale image.")
    
    try:
        # Initialize dlib's face detector and shape predictor
        detector = dlib.get_frontal_face_detector()
        predictor_path = "shape_predictor_68_face_landmarks.dat"
        
        # Check if the predictor file exists
        if not os.path.exists(predictor_path):
            raise FileNotFoundError(
                f"Shape predictor file '{predictor_path}' not found. "
                "Please download it from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
            )
            
        predictor = dlib.shape_predictor(predictor_path)
        
        # Detect faces
        faces = detector(gray, 1)  # The 1 means to upsample the image once
        
        if not faces:
            return None, None
            
        # Get landmarks for the first face
        landmarks = predictor(gray, faces[0])
        return faces[0], landmarks
        
    except Exception as e:
        st.error(f"Error in face detection: {str(e)}")
        return None, None

def warp_triangle(img1: np.ndarray, img2: np.ndarray, t1: np.ndarray, t2: np.ndarray) -> None:
    """Warp a triangle from one image to another.
    
    Args:
        img1: Source image
        img2: Destination image (will be modified)
        t1: Source triangle points (3 points)
        t2: Destination triangle points (3 points)
    """
    # Convert to float32 for calculations
    t1 = np.float32(t1)
    t2 = np.float32(t2)
    
    # Get bounding rectangles for the triangles
    r1 = cv2.boundingRect(t1)
    r2 = cv2.boundingRect(t2)
    
    # Get points relative to the bounding rectangles
    t1_rect = []
    t2_rect = []
    t2_rect_int = []
    
    for i in range(3):
        t1_rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2_rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2_rect_int.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
    
    # Create a mask for the triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2_rect_int), (1.0, 1.0, 1.0), 16, 0)
    
    # Get the region of interest from the source image
    img1_rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    
    # Warp the triangle
    size = (r2[2], r2[3])
    mat = cv2.getAffineTransform(np.float32(t1_rect), np.float32(t2_rect))
    warp = cv2.warpAffine(img1_rect, mat, size, None, flags=cv2.INTER_LINEAR, 
                         borderMode=cv2.BORDER_REFLECT_101)
    
    # Blend the warped triangle with the destination image
    img2_rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]
    img2_rect = img2_rect * (1 - mask) + warp * mask
    
    # Put the blended triangle back into the destination image
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2_rect

def swap_faces(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    """Swap faces between two images.
    
    Args:
        img1: First image (source face)
        img2: Second image (destination face)
        
    Returns:
        Image with swapped faces
    """
    # Make a copy of the second image to modify
    output = np.copy(img2)
    
    # Detect faces and landmarks
    _, landmarks1 = detect_landmarks(img1)
    _, landmarks2 = detect_landmarks(img2)
    
    if landmarks1 is None or landmarks2 is None:
        raise ValueError("Could not detect faces in one or both images")
    
    # Convert landmarks to numpy arrays
    points1 = np.array([[p.x, p.y] for p in landmarks1.parts()])
    points2 = np.array([[p.x, p.y] for p in landmarks2.parts()])
    
    # Get the convex hull for the second face
    hull2 = cv2.convexHull(points2, returnPoints=False)
    
    # Get the convex hull points for both faces
    hull_points1 = []
    hull_points2 = []
    
    for i in range(len(hull2)):
        hull_points1.append(points1[hull2[i][0]])
        hull_points2.append(points2[hull2[i][0]])
    
    hull_points1 = np.array(hull_points1)
    hull_points2 = np.array(hull_points2)
    
    # Calculate the Delaunay triangulation
    rect = cv2.boundingRect(np.float32([hull_points2]))
    subdiv = cv2.Subdiv2D(rect)
    subdiv.insert([tuple(p) for p in hull_points2])
    
    triangles = subdiv.getTriangleList()
    triangles = np.array(triangles, dtype=np.int32)
    
    # Warp each triangle from the first face to the second face
    for t in triangles:
        pts2 = []
        pts1 = []
        
        for i in range(3):
            pt = (t[2 * i], t[2 * i + 1])
            # Find the index of the point in the convex hull
            idx = np.where((hull_points2 == pt).all(axis=1))[0]
            if len(idx) == 0:
                continue
            pts2.append(pt)
            pts1.append(hull_points1[idx[0]])
        
        if len(pts1) == 3 and len(pts2) == 3:
            warp_triangle(img1, output, np.array(pts1), np.array(pts2))
    
    return output

def show_face_swap_ui():
    """Display the Streamlit UI for the Face Swap feature."""
    st.markdown("### 😆 Face Swap")
    
    # Check dependencies
    deps_ok, deps_msg = check_dependencies()
    if not deps_ok:
        st.error(deps_msg)
        return
    
    st.info("ℹ️ Upload two images with clear frontal faces to swap them.")
    
    # Create two columns for the image uploaders
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Face 1")
        img1_file = st.file_uploader(
            "Upload first face", 
            type=['jpg', 'jpeg', 'png'],
            key="face1"
        )
        
        if img1_file is not None:
            st.image(img1_file, caption="Face 1", use_column_width=True)
    
    with col2:
        st.markdown("#### Face 2")
        img2_file = st.file_uploader(
            "Upload second face", 
            type=['jpg', 'jpeg', 'png'],
            key="face2"
        )
        
        if img2_file is not None:
            st.image(img2_file, caption="Face 2", use_column_width=True)
    
    # Add a button to perform the face swap
    if st.button("🔄 Swap Faces", type="primary"):
        if img1_file is None or img2_file is None:
            st.error("❌ Please upload both images first!")
            return
            
        with st.spinner("🔍 Detecting faces and performing swap..."):
            try:
                # Debug: Show file information
                st.sidebar.write("Debug Info:")
                st.sidebar.write(f"File 1 type: {type(img1_file)}")
                st.sidebar.write(f"File 2 type: {type(img2_file)}")
                
                # Load and prepare both images
                img1, img1_path = load_and_prepare_image(img1_file)
                img2, img2_path = load_and_prepare_image(img2_file)
                
                if img1 is None or img2 is None:
                    st.error("❌ Failed to load one or both images. Please try different images.")
                    return
                
                # Debug: Show image shapes
                st.sidebar.write(f"Image 1 shape: {img1.shape if img1 is not None else 'None'}")
                st.sidebar.write(f"Image 2 shape: {img2.shape if img2 is not None else 'None'}")
                
                # Check if the shape predictor file exists
                predictor_path = "shape_predictor_68_face_landmarks.dat"
                if not os.path.exists(predictor_path):
                    st.error(
                        f"❌ Shape predictor file '{predictor_path}' not found.\n"
                        "Please download it from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2\n"
                        "Extract the .dat file and place it in the same directory as this script."
                    )
                    return
                
                # Try to detect faces in both images
                st.sidebar.write("Detecting faces...")
                face1, landmarks1 = detect_landmarks(img1)
                face2, landmarks2 = detect_landmarks(img2)
                
                if face1 is None or landmarks1 is None:
                    st.error("❌ Could not detect a face in the first image. Please use a clear frontal face photo.")
                    st.image(img1, caption="First Image (No Face Detected)", use_column_width=True, channels="RGB")
                    return
                    
                if face2 is None or landmarks2 is None:
                    st.error("❌ Could not detect a face in the second image. Please use a clear frontal face photo.")
                    st.image(img2, caption="Second Image (No Face Detected)", use_column_width=True, channels="RGB")
                    return
                
                st.sidebar.write("Performing face swap...")
                # Perform the face swap
                result = swap_faces(img1, img2)
                
                if result is not None:
                    # Convert back to BGR for displaying with OpenCV
                    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
                    
                    # Display the result
                    st.success("✅ Face swap completed successfully!")
                    
                    # Show before/after comparison
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        st.image(img1, caption="Original Face 1", use_column_width=True, channels="RGB")
                    with col2:
                        st.image(img2, caption="Original Face 2", use_column_width=True, channels="RGB")
                    with col3:
                        st.image(result, caption="Swapped Result", use_column_width=True, channels="RGB")
                    
                    # Add a download button
                    _, buffer = cv2.imencode('.jpg', result_bgr)
                    st.download_button(
                        label="💾 Download Result",
                        data=buffer.tobytes(),
                        file_name="face_swap_result.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.error("❌ Face swap failed. Please try with different images.")
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                import traceback
                st.text(traceback.format_exc())  # Show full traceback for debugging
    
    # Add some helpful information
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        ### Face Swap Guide
        1. Upload two images with clear frontal faces
        2. Click the 'Swap Faces' button
        3. View and download the result
        
        **Tips for best results:**
        - Use well-lit, high-quality images
        - Ensure faces are clearly visible and not obstructed
        - Frontal faces work best (not at an angle)
        - Avoid extreme facial expressions
        
        **Note:** This is a basic implementation. For better results, consider using more advanced face swapping libraries.
        """)
