import cv2
import numpy as np
import os
dataset_path = r"C:\Users\Lenovo\OneDrive\Desktop\Image Recog\Image dataset\att_faces"
def load_images(directory):
    images = []
    labels = []
    label_dict = {}

    subfolders = sorted(os.listdir(directory))
    # subfolder is the list of folders containg images of each person
    for label_id, folder in enumerate(subfolders):
        folder_path = os.path.join(directory,folder)
        if os.path.isdir(folder_path):
            label_dict[label_id] = folder
            # we have mapped all face ids to their respective names in label_dict
            for image_name in os.listdir(folder_path):
                 if image_name.endswith('.pgm'):
                     image_path = os.path.join(folder_path , image_name) 
                     img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
                     #imread reads the image in grayscale mode
                     img = cv2.resize(img,(100,100))
                     images.append(img.flatten())
                     labels.append(label_id)
    return np.array(images),np.array(labels),label_dict

def compute_pca(images, num_components = 50):
    mean_face = np.mean(images,axis = 0)
    centered_images = images - mean_face

    covariance_matrix = np.dot(centered_images.T,centered_images)     #Multiplication of centered_images with his transpose 
    eigenvalues , eigenvector = np.linalg.eigh(covariance_matrix)

    idx = np.argsort(-eigenvalues)[:num_components]
    eigenfaces = eigenvector[:,idx]

    return mean_face, eigenfaces

def project_face(image,mean_face,eigen_faces):
    return np.dot(eigen_faces.T,(image - mean_face))

def recognize_face(test_image,mean_face,eigen_faces,images,labels,label_dict):
    test_image = cv2.resize(test_image,(100,100)).flatten()

    projected_test = project_face(test_image,mean_face,eigen_faces)
    projected_train = np.dot(images - mean_face,eigen_faces)
    
    distances = np.linalg.norm(projected_train - projected_test,axis = 1)

    best_match = np.argmin(distances)

    return label_dict[labels[best_match]], distances[best_match]



if __name__ == "__main__":
    images,labels ,labl_dict = load_images(dataset_path)
    mean_face,eigenface = compute_pca(images)
    
    test_img_path = r"C:\Users\Lenovo\OneDrive\Pictures\Saved Pictures\licensed-imag676e.xcf"
    test_image = cv2.imread(test_img_path,cv2.IMREAD_GRAYSCALE)

    result,distance = recognize_face(test_image,mean_face,eigenface,images,labels,labl_dict)
    if distance <= 500:
        print(f"Recognized as: {result}")
        print(f"Distance: {distance:.2f}")
    else:
        print(f"Image is not Recognized But available at a Distance: {distance:.2f} in {result}")
