import random
import re
import warnings


def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


def parse_names(data):
    parsed_names = re.findall(r'\|\s*([A-Za-z]+)\s*\|', data, re.DOTALL)
    parsed_names = [name.strip() for name in parsed_names]

    if parsed_names:
        return parsed_names[1:]
    else:
        warnings.warn("List of names is empty. Check content of names markdown file")
        return []


def parse_locations(data):
    parsed_locations = re.findall(r'\|\s*([0-9]+)\s*\|\s*([A-Za-z,\s, \(,\)]+)\|', data, re.DOTALL)
    parsed_locations = [b for (a, b) in parsed_locations]
    parsed_locations = [location.strip() for location in parsed_locations]

    parsed_placement_locations = [location for location in parsed_locations if location.endswith('(p)')]
    parsed_locations = [location.replace('(p)', '') for location in parsed_locations]
    parsed_placement_locations = [location.replace('(p)', '') for location in parsed_placement_locations]
    parsed_placement_locations = [location.strip() for location in parsed_placement_locations]


    if parsed_locations:
        return parsed_locations, parsed_placement_locations
    else:
        warnings.warn("List of locations is empty. Check content of location markdown file")
        return []


def parse_rooms(data):
    parsed_rooms = re.findall(r'\|\s*(\w+ \w*)\s*\|', data, re.DOTALL)
    parsed_rooms = [rooms.strip() for rooms in parsed_rooms]

    if parsed_rooms:
        return parsed_rooms[1:]
    else:
        warnings.warn("List of rooms is empty. Check content of room markdown file")
        return []


def parse_objects(data):
    parsed_objects = re.findall(r'\|\s*(\w+)\s*\|', data, re.DOTALL)
    parsed_objects = [objects for objects in parsed_objects if objects != 'Objectname']
    parsed_objects = [objects.replace("_", " ") for objects in parsed_objects]
    parsed_objects = [objects.strip() for objects in parsed_objects]

    parsed_categories = re.findall(r'# Class \s*([A-Za-z,\s]+)\s*', data, re.DOTALL)
    parsed_categories = [category.strip() for category in parsed_categories]
    parsed_categories = [category.strip() for category in parsed_categories]

    if parsed_objects or parsed_categories:
        return parsed_objects, parsed_categories
    else:
        warnings.warn("List of objects or object categories is empty. Check content of object markdown file")
        return []


def generate_command(person_names, location_names, placement_location_names, room_names, object_names,
                     object_categories):
    command_type = random.choice(['Move', 'Find'])
    move_verbs = ["Move", "Bring"]
    find_verbs = ["Find", "Locate"]
    location_preps = ["in", "at"]

    if command_type == 'Move':
        verb = random.choice(move_verbs)
        subject = random.choice(object_names)
        source = random.choice(placement_location_names + room_names)
        destination = random.choice(placement_location_names)
        return f"{verb} the {subject} from the {source} to the {destination}"
    elif command_type == 'Find':
        verb = random.choice(find_verbs)
        person = random.choice(person_names)
        prep = random.choice(location_preps)
        if prep == "in":
            location = random.choice(room_names)
        else:
            location = random.choice(location_names)
        object_class = random.choice(object_categories)
        return f"{verb} {person} {prep} the {location} and find a {object_class}"


if __name__ == "__main__":
    names_file_path = '../names/names.md'
    locations_file_path = '../maps/location_names.md'
    rooms_file_path = '../maps/room_names.md'
    objects_file_path = '../objects/test.md'

    names_data = read_data(names_file_path)
    names = parse_names(names_data)

    locations_data = read_data(locations_file_path)
    location_names, placement_location_names = parse_locations(locations_data)

    rooms_data = read_data(rooms_file_path)
    room_names = parse_rooms(rooms_data)

    objects_data = read_data(objects_file_path)
    object_names, object_categories = parse_objects(objects_data)

    for _ in range(50):  # Generate 5 random commands
        command = generate_command(names, location_names, placement_location_names, room_names, object_names,
                                   object_categories)
        print(command)
