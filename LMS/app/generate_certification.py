import os
import cv2

list_of_names = []

cur_path = os.getcwd()
# # print(cur_path)
path = cur_path + "\Media\certificate"
# def delete_old_data():
#     for i in os.listdir(path+"generated-certificates/"):
#         os.remove(path+"generated-certificates/{}".format(i))


def cleanup_data():
    with open('name-data.txt') as f:
        for line in f:
            list_of_names.append(line.strip())

def generate_certificates(name, courseName, date, id, instructor):
    cur_path = os.path.dirname(os.getcwd())
    path = cur_path + "\LMS\Media\certificate"
    # prints all files
    # path = "Media/certificate"
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 0.9
    color_blue = (255, 0, 0)
    color_red = (0, 0, 255)
    color_black = (0, 0, 0)
    thickness = 0
    line_type = cv2.LINE_AA

    # Get the dimensions of the text
    text_width, text_height = cv2.getTextSize(name, font, font_scale, thickness)[0]
    print(text_width, text_height)
    # calculate the position to center the text
    text_center_x = (360 - text_width) // 2
    text_center_y = (40 - text_height) // 2

    certificate_template_image = cv2.imread(path + "\certificate-template.jpeg")

    cv2.putText(certificate_template_image, name.strip(), (160 + text_center_x, 290 + text_center_y), font, font_scale, (20, 90, 50 ), thickness, line_type)

    font_scale = 0.5
    text_width, text_height = cv2.getTextSize(courseName, font, font_scale, thickness)[0]
    print(text_width, text_height)
    # calculate the position to center the text
    text_center_x = (360 - text_width) // 2
    text_center_y = (40 - text_height) // 2
    cv2.putText(certificate_template_image,
                "Congratulations on successfully completing",
                (170 + text_center_x, 320 + text_center_y), font, font_scale, color_black, thickness, line_type)
    cv2.putText(certificate_template_image,
                courseName.strip() ,
                (170 + text_center_x, 350 + text_center_y), font, font_scale, color_black, thickness, line_type)

    font_scale = 0.85
    line_type = cv2.LINE_AA
    thickness = 0
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    text_width, text_height = cv2.getTextSize(date, font, font_scale, thickness)[0]
    print(text_width, text_height)
    # calculate the position to center the text
    text_center_x = (92 - text_width) // 2
    text_center_y = (18 - text_height) // 2
    cv2.putText(certificate_template_image, date.strip(), (330 + text_center_x, 110 + text_center_y), font, 0.6, color_black, 1, line_type)
    cv2.putText(certificate_template_image, "Edward Bui", (165 + text_center_x, 420 + text_center_y), font, font_scale,
                color_black, thickness, line_type)
    cv2.putText(certificate_template_image, instructor.strip(), (480 + text_center_x, 420 + text_center_y), font, font_scale,
                color_black, thickness, line_type)
    cv2.imwrite(path+"/generated-certificates/{}.jpeg".format(id), certificate_template_image)

# def main():
#     # delete_old_data()
#     # cleanup_data()
#     # generate_certificates("Pat N. Joffis", "Python for beginners", "2023-06-04", "1234")
#     generate_certificates("AAAAAAAAAAAAA", "AAAAAAAAAAAAAAAAAA", "2023-06-06", "456", "Manh Cuong")
#
# if __name__ == '__main__':
#     main()
