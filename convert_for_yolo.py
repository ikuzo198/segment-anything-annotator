import os
import json
import sys
import glob


def write_coco_segmentation(json_file, output_file, width, height):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    annotations = data['shapes']

    with open(output_file, 'w') as f:
        for annotation in annotations:
            annotation_id = label2id
            segmentation = annotation['points'][0]

            adjusted_segmentation = []
            for i, coord in enumerate(segmentation):
                if i % 2 == 0:
                    adjusted_coord = coord / width
                else:
                    adjusted_coord = coord / height
                adjusted_segmentation.append(adjusted_coord)

            adjusted_segmentation = str(adjusted_segmentation)[1:-1]
            adjusted_segmentation = adjusted_segmentation.replace(",","")
            f.write(f"{annotation_id} {adjusted_segmentation}\n")


def process_json_files(folder, width, height):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                output_file = os.path.join(root, os.path.splitext(file)[0] + '.txt')
                write_coco_segmentation(json_file, output_file, width, height)
                print(f"Processed: {json_file} -> {output_file}")


def create_txt_file(id, points):
    """idと座標をまとめてテキスト形式で書き出す
    """
    pass
    


def get_points(path="/outputs/test/multiclass.json", width=640, height=480):
    """rawデータから学習に使用する座標を取得する
    json_file_path: jsonファイルのパス
    """
    json_file_path = os.getcwd() + path

    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    annotations = data['shapes']

    with open("outputs/test/test.txt", "w", newline='\n') as f:
        for annotation in annotations:
            object_wise_data = [] 
            id = label2id(annotation["label"])
            # object_wise_data.append(id)

            for point in annotation["points"]:
                shapes = []

                point_x = point[0] / width
                point_y = point[1] / height

                object_wise_data.append(point_x)
                object_wise_data.append(point_y)

            adjusted_segmentation = str(object_wise_data)[1:-1]
            adjusted_segmentation = adjusted_segmentation.replace(",","")
            f.write(f"{id} {adjusted_segmentation}\n")

    pass


def label2id(label)-> int:
    """クラス名からidを返す
    """
    id = load_class_json()[label]
    # print(id)
    return id


def load_class_json(path='/inputs/class-names.json')-> dict:
    """クラス名が書いてあるjsonを読み込んでdict型で返す
    """
    data_path = os.getcwd() + path

    with open(data_path, "r") as f:
        raw_data = json.load(f)

    class_names_dict:dict = {}

    for i, name in enumerate(raw_data["names"]):
        class_names_dict[name] = i
    
    # print(class_names_dict)

    return class_names_dict


def test():
    data = get_points(width=960, height=640)
    label2id("baby_buggy")


if __name__ == "__main__":
    test()
    # if len(sys.argv) < 2:
    #     print("Please provide the folder path as arguments.")
    #     sys.exit(1)

    # folder_path = sys.argv[1]
    # # width = int(sys.argv[2])
    # # height = int(sys.argv[3])
    # width = 640
    # height = 480
    # process_json_files(folder_path, width, height)
