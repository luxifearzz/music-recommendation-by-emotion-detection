import os
import json

# -- Tools Zone --
def update_ratings_tools(music_directory, new_rating, new_total_ratings):
    cnt = 0
    for root, dirs, files in os.walk(music_directory):
        # print(f"Checking directory: {root}")  # Print the current directory being checked
        for file in files:
            # print(f"Found file: {file}")  # Print the files found
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                # Rest of your code...
                with open(file_path, 'r') as f:
                    data = json.load(f)

                if data['rating'] == new_rating:
                    continue

                # Debug print before update
                print(f"Updating {file_path}: current rating = {data['rating']}, total_ratings = {data['total_ratings']}")

                # Update rating and total_ratings
                data['rating'] = new_rating
                data['total_ratings'] = new_total_ratings

                # Write the updated data back to the file
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                    
                cnt += 1
    return cnt

def update_json_value_tools(directory, field, new_str_format):
    cnt = 0
    # ตรวจสอบทุกไฟล์ในโฟลเดอร์ที่กำหนด
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # เปลี่ยนค่าในฟิลด์ "field"
                if field in data and isinstance(data[field], int):
                    data[field] = new_str_format(data[field])

                # บันทึกข้อมูลกลับลงในไฟล์
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    
                cnt += 1
    return cnt

# -- Usage Zone --
def update_ratings():
    music_directory = 'backend/my_flask_api/music'  # Path to your music directory
    new_rating = 0  # Set the new rating value
    new_total_ratings = 0  # Set the new total ratings value

    change_cnt = update_ratings_tools(music_directory, new_rating, new_total_ratings)
    
    print(f"Update rating for {change_cnt} files successfully")
    
def update_json_value():
    music_directory = 'backend/my_flask_api/music'  # Path to your music directory
    field = 'id'
    new_str_format = lambda val: f"song{val}"

    change_cnt = update_json_value_tools(music_directory, field, new_str_format)
    
    print(f"Update field \"{field}\" to format \"{new_str_format("{val}")}\" for {change_cnt} files successfully")

if __name__ == "__main__":

    # update_ratings()
    
    update_json_value()
