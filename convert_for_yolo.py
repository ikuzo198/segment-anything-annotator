import os
import json
import sys
import glob
import argparse


def process_json_files(folder, class_path, width, height):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                output_file = os.path.join(root, os.path.splitext(file)[0] + '.txt')
                get_points(json_file, class_path, output_file, width, height)
                print(f"Processed: {json_file} -> {output_file}")


def get_points(json_file="multiclass.json", class_list="inputs/class-names.json", output_file="output.txt", width=640, height=480):
    """rawデータからsegmentデータを取得しtxt形式で書き出す
    json_file: jsonファイル名
    """
    json_file_path = json_file

    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    annotations = data['shapes']

    with open(output_file, "w", newline='\n') as f:
        for annotation in annotations:
            object_wise_data = [] 
            id = load_class_json(class_list)[annotation["label"]]

            for point in annotation["points"]:
                shapes = []

                point_x = point[0] / width
                point_y = point[1] / height

                object_wise_data.append(point_x)
                object_wise_data.append(point_y)

            adjusted_segmentation = str(object_wise_data)[1:-1]
            adjusted_segmentation = adjusted_segmentation.replace(",","")
            f.write(f"{id} {adjusted_segmentation}\n")


def load_class_json(path='/inputs/class-names.json')-> dict:
    """クラス名が書いてあるjsonを読み込んでdict型で返す
    """
    data_path = os.getcwd() + path

    with open(data_path, "r") as f:
        raw_data = json.load(f)

    class_names_dict:dict = {}

    for i, name in enumerate(raw_data["names"]):
        class_names_dict[name] = i

    return class_names_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=640,
                        help='image width')
    parser.add_argument('--height', type=int, default=480,
                        help='image height')
    parser.add_argument('--class_path', type=str, default='/inputs/class-names.json',
                        help='クラス名が書いてあるjsonファイルのパスとファイル名')
    parser.add_argument('--target', type=str, default='dataset/',
                        help='変換したいデータセットへのパス')
    args = parser.parse_args()

    # data = get_points(width=args.width, height=args.height)
    process_json_files(args.target, args.class_path, args.width, args.height)

