import cv2
import numpy as np
import pyzed.sl as sl

def main():
    # Initialisation de la caméra ZED
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # Qualité max de la profondeur
    init_params.coordinate_units = sl.UNIT.MILLIMETER

    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(f"Erreur d'ouverture de la caméra : {status}")
        exit(1)

    # Création des objets pour stocker les images
    image = sl.Mat()
    depth = sl.Mat()

    print("Appuyez sur 'q' pour quitter.")

    while True:
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)

            img_np = image.get_data()
            depth_np = depth.get_data()

            # Normaliser l’image de profondeur pour l'affichage
            depth_display = cv2.normalize(depth_np, None, 0, 255, cv2.NORM_MINMAX)
            depth_display = np.uint8(depth_display)

            # Affichage des deux images
            cv2.imshow("Image ZED", img_np)
            cv2.imshow("Profondeur", depth_display)

            # Quitter avec 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Libération
    cv2.destroyAllWindows()
    zed.close()

if __name__ == "__main__":
    main()
