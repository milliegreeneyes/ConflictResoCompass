import os
import glob
import json
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib
import textwrap

matplotlib.use('TkAgg')  # Use the TkAgg backend (adjust as needed for your system)


# Function to compare conflict resolution styles between two individuals
def compare():
    cls()
    print("You selected 'Compare'.")

    # Function to get a valid name input from the user
    def get_name_input(prompt):
        while True:
            name_prefix = input(prompt).strip().lower()
            if len(name_prefix) >= 3:
                return name_prefix[:3]
            else:
                print("Please enter at least 3 characters for the name prefix.")

    name_prefix1 = get_name_input("Enter the first 3 letters of the first person's name: ")
    name_prefix2 = get_name_input("Enter the first 3 letters of the second person's name: ")

    # Find matching JSON files for both individuals
    file_list1 = glob.glob(f"conflictjsons/{name_prefix1}*.json")
    file_list2 = glob.glob(f"conflictjsons/{name_prefix2}*.json")

    if not file_list1:
        print(f"No matching files found for the first person with prefix '{name_prefix1}'.")
        return

    if not file_list2:
        print(f"No matching files found for the second person with prefix '{name_prefix2}'.")
        return

    # Display matching files for both individuals
    print(f"Matching files for the first person ({name_prefix1}):")
    for i, file_path in enumerate(file_list1, start=1):
        print(f"{i}: {os.path.splitext(os.path.basename(file_path))[0]}")

    print(f"Matching files for the second person ({name_prefix2}):")
    for i, file_path in enumerate(file_list2, start=1):
        print(f"{i}: {os.path.splitext(os.path.basename(file_path))[0]}")

    while True:
        try:
            selection1 = int(input(f"Select a file for the first person (1-{len(file_list1)}): "))
            if 1 <= selection1 <= len(file_list1):
                break
            else:
                print("Invalid selection for the first person. Please enter a valid number.")
        except ValueError:
            print("Invalid input for the first person. Please enter a valid number.")

    while True:
        try:
            selection2 = int(input(f"Select a file for the second person (1-{len(file_list2)}): "))
            if 1 <= selection2 <= len(file_list2):
                break
            else:
                print("Invalid selection for the second person. Please enter a valid number.")
        except ValueError:
            print("Invalid input for the second person. Please enter a valid number.")

    selected_file_path1 = file_list1[selection1 - 1]
    selected_file_path2 = file_list2[selection2 - 1]

    cls()

    # Load JSON data for both individuals
    with open(selected_file_path1, 'r') as file1:
        json_data1 = json.load(file1)

    with open(selected_file_path2, 'r') as file2:
        json_data2 = json.load(file2)

    # print("Contents of selected JSON file for the first person:")
    # print(json.dumps(json_data1, indent=4))
    #
    # print("\nContents of selected JSON file for the second person:")
    # print(json.dumps(json_data2, indent=4))

    # Extract conflict resolution style data for both individuals
    style_data1 = json_data1.get('the_values', [])
    style_data2 = json_data2.get('the_values', [])

    name1 = json_data1.get('name', 'Unknown')
    name2 = json_data2.get('name', 'Unknown')

    # # Print the conflict resolution styles for both individuals
    # print(f"\nConflict Resolution Styles for {name1}:")
    # print(f"Values: {', '.join(map(str, style_data1))}")
    # print(f"Max: {json_data1.get('the_max', 'N/A')}")
    # print(f"Secondaries: {json_data1.get('the_secondaries', 'N/A')}")
    # print(f"Leasts: {json_data1.get('the_leasts', 'N/A')}")
    #
    # print(f"\nConflict Resolution Styles for {name2}:")
    # print(f"Values: {', '.join(map(str, style_data2))}")
    # print(f"Max: {json_data2.get('the_max', 'N/A')}")
    # print(f"Secondaries: {json_data2.get('the_secondaries', 'N/A')}")
    # print(f"Leasts: {json_data2.get('the_leasts', 'N/A')}")

    # Compare the conflict resolution styles
    print("\nComparing Conflict Resolution Styles:")

    # Mapping of styles to their descriptions
    style_descriptions = {
        "accommodating": "You tend to accommodate the wishes of others.",
        "avoiding": "You often avoid conflicts and uncomfortable situations.",
        "collaborating": "You actively seek collaboration and problem-solving.",
        "competing": "You argue your case and insist on the merits of your point of view.",
        "compromising": "You prefer to compromise when solving problems."
    }

    print(f"Conflict resolution styles for {name1} and {name2}: ")

    # Determine the prominent and secondary styles for both individuals
    def get_prominent_styles(data):
        styles = ["Accommodating", "Avoiding", "Collaborating", "Competing", "Compromising"]
        style_values = dict(zip(styles, data))
        sorted_styles = sorted(styles, key=lambda x: style_values[x], reverse=True)
        return sorted_styles[:2]  # Return the top 2 styles

    def are_2nd_and_3rd_equal(numbers):
        # Check if the list has at least 3 elements
        sorted_nums = sorted(numbers, reverse=True)
        if len(numbers) >= 3:
            # Compare the 2nd and 3rd elements
            if sorted_nums[1] == sorted_nums[2]:
                return True
        # If the list doesn't meet the conditions or the elements are not equal, return False
        return False

    def get_zero_and_index2_styles(data):
        styles = ["Accommodating", "Avoiding", "Collaborating", "Competing", "Compromising"]
        style_values = dict(zip(styles, data))
        sorted_styles = sorted(styles, key=lambda x: style_values[x], reverse=True)
        return [sorted_styles[0], sorted_styles[2]]  # Return the styles at 0 index and 2 index

    ans1 = are_2nd_and_3rd_equal(style_data1)

    prominent_styles1 = get_prominent_styles(style_data1)
    prominent_styles1_b = []
    if ans1:
        prominent_styles1_b = get_zero_and_index2_styles(style_data1)

    ans2 = are_2nd_and_3rd_equal(style_data2)

    prominent_styles2 = get_prominent_styles(style_data2)
    prominent_styles2_b = []
    if ans2:
        prominent_styles2_b = get_zero_and_index2_styles(style_data2)

    print(f"\nProminent Styles for {name1}:")
    print(textwrap.fill("\t" + ", ".join(prominent_styles1), width=70))
    if len(prominent_styles1_b) > 0:
        print(textwrap.fill("\tand " + ", ".join(prominent_styles1_b), width=70))
    print(f"Prominent Styles for {name2}:")
    print(textwrap.fill("\t" + ", ".join(prominent_styles2), width=70))
    if len(prominent_styles2_b) > 0:
        print(textwrap.fill("\tand " + ", ".join(prominent_styles2_b), width=70))

    print("\n")
    key_look_up = (prominent_styles1[0], prominent_styles1[1], prominent_styles2[0], prominent_styles2[1])
    print(key_look_up)

    # Check if the key exists in the dictionary before accessing it
    if key_look_up in best_combinations:
        value_for_key = best_combinations[key_look_up]
        print(textwrap.fill(value_for_key, width=70))

    # Check if prominent_styles1_b has values before accessing the dictionary
    if len(prominent_styles1_b) > 0:
        print("\n")
        key_look_up1_b = (prominent_styles1_b[0], prominent_styles1_b[1], prominent_styles2[0], prominent_styles2[1])
        print(key_look_up1_b)
        if key_look_up1_b in best_combinations:
            value_for_key1_b = best_combinations[key_look_up1_b]
            print(textwrap.fill(value_for_key1_b, width=70))

    # Check if prominent_styles2_b has values before accessing the dictionary
    if len(prominent_styles2_b) > 0:
        print("\n")
        key_look_up2_b = (prominent_styles1[0], prominent_styles1[1], prominent_styles2_b[0], prominent_styles2_b[1])
        print(key_look_up2_b)
        if key_look_up2_b in best_combinations:
            value_for_key2_b = best_combinations[key_look_up2_b]
            print(textwrap.fill(value_for_key2_b, width=70))

    print("\n")
    # Determine the ratings for the relationship
    relationship_ratings = {
        ("accommodating", "avoiding"): 4,
        ("accommodating", "accommodating"): 4,
        ("accommodating", "collaborating"): 6,
        ("accommodating", "competing"): 3,
        ("accommodating", "compromising"): 5,
        ("avoiding", "avoiding"): 3,
        ("avoiding", "accommodating"): 4,
        ("avoiding", "collaborating"): 5,
        ("avoiding", "competing"): 3,
        ("avoiding", "compromising"): 6,
        ("collaborating", "accommodating"): 6,
        ("collaborating", "avoiding"): 5,
        ("collaborating", "collaborating"): 8,
        ("collaborating", "competing"): 4,
        ("collaborating", "compromising"): 7,
        ("competing", "accommodating"): 3,
        ("competing", "avoiding"): 3,
        ("competing", "collaborating"): 4,
        ("competing", "competing"): 3,
        ("competing", "compromising"): 5,
        ("compromising", "compromising"): 7,
        ("compromising", "avoiding"): 6,
        ("compromising", "accommodating"): 5,
        ("compromising", "collaborating"): 7,
        ("compromising", "competing"): 5
    }

    relationship_rating = 0

    for style1 in prominent_styles1:
        for style2 in prominent_styles2:
            key = (style1.lower(), style2.lower())
            # rating = relationship_ratings.get(key, 0)
            rating = relationship_ratings[key]
            print(f"Key: {key}, Rating: {rating}")
            relationship_rating += rating

    # for style1 in prominent_styles1:
    #     for style2 in prominent_styles2:
    #         key = (style1, style2)
    #         relationship_rating += relationship_ratings.get(key, 0)

    print("\nRelationship Rating:")
    print(f"Total: {relationship_rating}")


    # # this is wrong
    # # Check if both individuals have equal secondaries
    # if json_data1.get('the_secondaries') == json_data2.get('the_secondaries'):
    #     shared_secondaries = json_data1.get('the_secondaries', 'N/A')
    #     print(f"\nBoth individuals have equal secondaries:")
    #     print(textwrap.fill(shared_secondaries, width=70))
    #
    #     # this is wrong
    #     # Get the best combinations for the shared secondaries
    #     # todo please explain why the following code only has "collaborating", "competing", "compromising",
    #     combinations = ("collaborating", "competing", "compromising", shared_secondaries)
    #     analysis1 = best_combinations.get(combinations, "No analysis available for this combination")
    #     analysis2 = best_combinations.get(combinations, "No analysis available for this combination")
    #
    #     print("\nAnalysis for Person 1:")
    #     print(textwrap.fill(analysis1, width=70))
    #
    #     print("\nAnalysis for Person 2:")
    #     print(textwrap.fill(analysis2, width=70))
    # else:
    #     # Get the best combinations for the prominent styles
    #     combinations1 = (*prominent_styles1, *prominent_styles2)
    #     combinations2 = (*prominent_styles2, *prominent_styles1)
    #     # todo I would have to make a separate best_combinations and switch person 1 with person 2
    #
    #     analysis1 = best_combinations.get(combinations1, "No analysis available for this combination")
    #     analysis2 = best_combinations.get(combinations2, "No analysis available for this combination")
    #
    #     print("\nAnalysis for Person 1:")
    #     print(textwrap.fill(analysis1, width=70))
    #
    #     print("\nAnalysis for Person 2:")
    #     print(textwrap.fill(analysis2, width=70))


# Dictionary of best combinations person 1 with person 2
best_combinations = {
    ("avoiding", "accommodating", "avoiding",
     "collaborating"): "In their relationship, Person 1 tends to avoid conflicts, while Person 2 is more accommodating and collaborative. This dynamic can be positive because it allows them to navigate disagreements without escalating tensions. However, there might be instances where Person 1's avoidance leads to unresolved issues, and Person 2 may feel that they give in too often.",
    ("avoiding", "accommodating", "avoiding",
     "competing"): "Person 1 avoids conflicts and accommodates the preferences of Person 2, who tends to avoid conflicts but may occasionally compete. This dynamic could create harmony in their relationship most of the time, but if Person 2's competitive style emerges too frequently, it might lead to frustration for Person 1.",
    ("avoiding", "accommodating", "avoiding",
     "compromising"): "Person 1 avoids conflicts and accommodates, while Person 2 avoids conflicts and is more inclined to compromise. This dynamic can promote cooperation and prevent major disagreements from arising. However, there is a risk that they might settle for middle-ground solutions that don't fully satisfy either party.",
    ("avoiding", "accommodating", "accommodating",
     "avoiding"): "In this relationship, Person 1 tends to avoid conflicts and accommodate, while Person 2 is also accommodating but occasionally resorts to avoidance. This balance between accommodation and avoidance can foster a peaceful coexistence, but it might result in unresolved issues if avoidance is used excessively by Person 2.",
    ("avoiding", "accommodating", "accommodating",
     "collaborating"): "Person 1 prefers avoiding conflicts and accommodating, while Person 2 leans towards accommodating and collaborating. This combination can lead to a harmonious relationship with open communication and collaboration during conflicts. However, there might be instances when Person 1's avoidance hinders full cooperation.",
    ("avoiding", "accommodating", "accommodating",
     "competing"): "In their relationship, Person 1 avoids conflicts and accommodates, while Person 2 also accommodates but may occasionally resort to competing. This dynamic can create a balance between cooperation and competition, but if Person 2's competitive style becomes dominant, it may lead to tension.",
    ("avoiding", "accommodating", "accommodating",
     "compromising"): "Person 1 avoids conflicts and accommodates, while Person 2 accommodates and is willing to compromise. This mix of styles can result in a cooperative and flexible relationship, as they are both open to finding middle-ground solutions. However, they should be careful not to compromise too much, which may lead to unmet needs.",
    ("avoiding", "accommodating", "collaborating",
     "avoiding"): "Person 1 avoids conflicts and accommodates, while Person 2 tends to collaborate but occasionally avoids confrontation. This combination can lead to effective problem-solving when collaboration occurs, but there may be moments of frustration if avoidance becomes the default approach for Person 2.",
    ("avoiding", "accommodating", "collaborating",
     "accommodating"): "In this relationship, Person 1 avoids conflicts and accommodates, while Person 2 is more inclined to collaborate and accommodate. This balance between accommodation and collaboration can foster effective communication and resolution of conflicts, but they should ensure that Person 1's avoidance doesn't hinder open discussions.",
    ("avoiding", "accommodating", "collaborating",
     "competing"): "Person 1 avoids conflicts and accommodates, while Person 2 tends to collaborate but may occasionally compete. This dynamic can create a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition to dominate, leading to potential conflicts.",
    ("avoiding", "accommodating", "collaborating",
     "compromising"): "In their relationship, Person 1 tends to avoid conflicts and accommodate, while Person 2's prominent styles are collaborating and compromising. This combination can lead to effective problem-solving through open communication and a willingness to find middle-ground solutions. Their ability to balance collaboration and compromise can create a positive dynamic in both daily interactions and the overall life of their relationship.",
    ("avoiding", "accommodating", "competing",
     "avoiding"): "Person 1's conflict resolution styles involve avoidance and accommodation, while Person 2 leans towards competing and avoiding. This dynamic may work well on a day-to-day basis as it prevents major conflicts, but in the long run, it might lead to unresolved issues and potential frustration for both individuals.",
    ("avoiding", "accommodating", "competing",
     "accommodating"): "Person 1 tends to avoid conflicts and accommodate, while Person 2's styles include competing and accommodating. This mix can create a balanced relationship where they navigate between cooperation and healthy competition. In their daily lives, they may have lively interactions, but it's important to ensure that competition doesn't overshadow cooperation.",
    ("avoiding", "accommodating", "competing",
     "collaborating"): "In their relationship, Person 1 avoids conflicts and accommodates, while Person 2 combines competing and collaborating. This combination can be dynamic and lead to diverse approaches to conflict resolution. In daily life, they may experience a mix of competition and collaboration, which can be both stimulating and challenging, depending on the situation.",
    ("avoiding", "accommodating", "competing",
     "compromising"): "Person 1's conflict resolution styles involve avoidance and accommodation, while Person 2 is inclined towards competing and compromising. This mix can create a dynamic relationship where they balance competition with a willingness to compromise. In daily life, they may face different challenges, but their ability to adapt can serve them well.",
    ("avoiding", "accommodating", "compromising",
     "avoiding"): "Person 1 tends to avoid conflicts and accommodate, while Person 2's styles include compromising and avoiding. This combination may help maintain peace in their daily interactions, but it's important to be cautious about settling for compromises that don't fully address their needs in the long-term.",
    ("avoiding", "accommodating", "compromising",
     "accommodating"): "In their relationship, Person 1 avoids conflicts and accommodates, while Person 2 emphasizes compromising and accommodating. This balance between accommodation and compromise can foster a flexible and cooperative dynamic in both daily interactions and the life of their relationship.",
    ("avoiding", "accommodating", "compromising",
     "collaborating"): "Person 1's conflict resolution styles involve avoidance and accommodation, while Person 2 prefers compromising and collaborating. This mix can create a harmonious relationship where they excel in finding middle-ground solutions while also collaborating effectively. In daily life, they may have productive discussions and outcomes.",
    ("avoiding", "accommodating", "compromising",
     "competing"): "In their relationship, Person 1 avoids conflicts and accommodates, while Person 2 combines compromising and competing. This dynamic can bring a mixture of cooperation and competition into their daily interactions and the overall life of their relationship. It's essential to manage the balance between these styles to ensure a healthy relationship.",
    ("avoiding", "collaborating", "avoiding",
     "accommodating"): "Person 1 tends to avoid conflicts and collaborate, while Person 2's prominent styles are avoidance and accommodation. This combination may result in effective conflict resolution through collaboration in daily life. However, there might be instances where Person 2's accommodating nature can lead to feelings of imbalance.",
    ("avoiding", "collaborating", "avoiding",
     "competing"): "Person 1 predominantly uses avoidance and collaboration as their conflict resolution styles, while Person 2 favors avoidance and competing. In daily life, Person 1's collaborative approach can promote open communication, but there may be challenges when Person 2's competitive style emerges, potentially causing tension. In the long term, their relationship may experience moments of harmony and conflict, depending on the balance of these styles.",
    ("avoiding", "collaborating", "avoiding",
     "compromising"): "Person 1's prominent styles are avoidance and collaboration, while Person 2 leans towards avoidance and compromising. This combination may lead to effective problem-solving through collaboration and compromise in their daily interactions. However, they should be cautious not to settle for compromises that do not fully address their needs over time.",
    ("avoiding", "collaborating", "accommodating",
     "avoiding"): "Person 1 prefers avoiding conflicts and collaborating, while Person 2's prominent styles are accommodating and avoidance. In their daily life, Person 1's collaborative nature may lead to open discussions, but they might face challenges if Person 2's avoidance hinders meaningful communication. Over time, they should work on addressing this potential barrier to maintain a healthy relationship.",
    ("avoiding", "collaborating", "accommodating",
     "collaborating"): "Person 1 predominantly uses avoidance and collaboration, while Person 2's styles involve accommodating and collaborating. This combination can foster effective communication and conflict resolution through collaboration in both daily interactions and the life of their relationship, leading to positive outcomes.",
    ("avoiding", "collaborating", "accommodating",
     "competing"): "Person 1's conflict resolution styles include avoidance and collaboration, while Person 2 combines accommodating and competing. In their daily life, they may experience a mix of collaboration and competition, which can be both stimulating and challenging, depending on the situation. They should manage this balance effectively to ensure a healthy relationship.",
    ("avoiding", "collaborating", "accommodating",
     "compromising"): "Person 1 tends to avoid conflicts and collaborate, while Person 2 leans towards accommodating and compromising. This combination can create a flexible and cooperative dynamic in their daily interactions and the life of their relationship. Their willingness to compromise and collaborate can lead to positive outcomes.",
    ("avoiding", "collaborating", "collaborating",
     "avoiding"): "In this relationship, Person 1 prefers avoiding conflicts and collaborating, while Person 2 has a prominent style of collaborating and avoiding. This dynamic may result in effective problem-solving through collaboration on certain occasions, but challenges may arise when avoidance becomes the default approach for Person 2, potentially hindering open discussions.",
    ("avoiding", "collaborating", "collaborating",
     "accommodating"): "Person 1 predominantly uses avoidance and collaboration, while Person 2 prefers collaborating and accommodating. This balance between collaboration and accommodation can promote effective communication and cooperation in both daily interactions and the life of their relationship.",
    ("avoiding", "collaborating", "collaborating",
     "competing"): "In their relationship, Person 1 tends to avoid conflicts and collaborate, while Person 2 combines collaborating and competing. This combination can create a dynamic where they alternate between collaboration and competition in their daily interactions. While it can be stimulating, they should manage the balance to prevent potential conflicts.",
    ("avoiding", "collaborating", "collaborating",
     "compromising"): "Person 1's conflict resolution styles involve avoidance and collaboration, while Person 2 emphasizes collaborating and compromising. This mix can create a harmonious relationship where they excel in finding middle-ground solutions through collaboration in both daily interactions and the life of their relationship.",
    ("avoiding", "collaborating", "competing",
     "avoiding"): "Person 1 primarily uses avoidance and collaboration as their conflict resolution styles, while Person 2 prefers competing and avoidance. In their daily life, Person 1's collaborative approach may lead to open communication, but challenges can arise when Person 2's competitive style surfaces, potentially causing tension. Over time, their relationship may experience moments of harmony and conflict, depending on how they manage these conflicting styles.",
    ("avoiding", "collaborating", "competing",
     "accommodating"): "Person 1's conflict resolution styles include avoidance and collaboration, while Person 2 leans towards competing and accommodating. In their daily interactions, they may experience a blend of collaboration and competition, which can be both stimulating and challenging. Managing this balance effectively is crucial for maintaining a healthy relationship.",
    ("avoiding", "collaborating", "competing",
     "collaborating"): "Person 1 primarily uses avoidance and collaboration, while Person 2 prefers competing and collaborating. This combination can lead to diverse approaches to conflict resolution in their daily life, with moments of collaboration and competition. It's important for them to navigate this dynamic effectively to prevent conflicts from becoming detrimental to their relationship.",
    ("avoiding", "collaborating", "competing",
     "compromising"): "In their relationship, Person 1 avoids conflicts and collaborates, while Person 2 combines competing and compromising. This dynamic can bring a mixture of cooperation and competition into their daily interactions and the overall life of their relationship. They should strive to manage the balance between these styles to ensure a healthy and harmonious relationship.",
    ("avoiding", "collaborating", "compromising",
     "avoiding"): "Person 1's conflict resolution styles involve avoidance and collaboration, while Person 2 emphasizes compromising and avoiding. In their daily life, Person 1's collaborative nature may lead to open discussions, but they might face challenges if Person 2's avoidance hinders meaningful communication. Over time, they should work on addressing this potential barrier to maintain a healthy relationship.",
    ("avoiding", "collaborating", "compromising",
     "accommodating"): "Person 1 tends to avoid conflicts and collaborate, while Person 2 leans towards compromising and accommodating. This combination can create a flexible and cooperative dynamic in their daily interactions and the life of their relationship. Their willingness to compromise and collaborate can lead to positive outcomes.",
    ("avoiding", "collaborating", "compromising",
     "collaborating"): "Person 1 primarily uses avoidance and collaboration, while Person 2 prefers compromising and collaborating. This balance between collaboration and accommodation can promote effective communication and cooperation in both daily interactions and the life of their relationship, leading to positive outcomes.",
    ("avoiding", "collaborating", "compromising",
     "competing"): "In their relationship, Person 1 tends to avoid conflicts and collaborate, while Person 2 combines compromising and competing. This dynamic can create a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition to dominate, leading to potential conflicts.",
    ("avoiding", "competing", "avoiding",
     "accommodating"): "Person 1 predominantly uses avoidance and competing as their conflict resolution styles, while Person 2 favors avoidance and accommodating. In their daily life, Person 1's competitive approach may lead to occasional tension, but Person 2's accommodating nature can help maintain harmony. Over time, they should find a balance between these styles to prevent conflicts from becoming more frequent.",
    ("avoiding", "competing", "avoiding",
     "collaborating"): "Person 1 tends to avoid conflicts and compete, while Person 2 prefers avoiding and collaborating. In their daily interactions, they may experience a mix of competition and collaboration, which can be both stimulating and challenging, depending on the situation. Managing this balance effectively is crucial for a healthy relationship.",
    ("avoiding", "competing", "avoiding",
     "compromising"): "Person 1 primarily uses avoidance and competing as their conflict resolution styles, while Person 2 prefers avoiding and compromising. In their daily life, Person 1's competitive approach may lead to occasional tension, but Person 2's compromising nature can help maintain harmony. Over time, they should find a balance between these styles to prevent conflicts from becoming more frequent.",
    ("avoiding", "competing", "accommodating",
     "avoiding"): "Person 1 tends to avoid conflicts and compete, while Person 2 has the prominent styles of accommodating and avoiding. In their daily interactions, they may experience a mix of competition and accommodation, which can be both stimulating and challenging. Managing this balance effectively is crucial for maintaining a healthy relationship.",
    ("avoiding", "competing", "accommodating",
     "collaborating"): "Person 1 primarily uses avoidance and competing, while Person 2 prefers accommodating and collaborating. This combination can lead to diverse approaches to conflict resolution in their daily life, with moments of competition and collaboration. It's important for them to navigate this dynamic effectively to prevent conflicts from becoming detrimental to their relationship.",
    ("avoiding", "competing", "accommodating",
     "competing"): "In their relationship, Person 1 tends to avoid conflicts and compete, while Person 2 combines accommodating and competing. This dynamic can bring a mixture of cooperation and competition into their daily interactions and the overall life of their relationship. They should strive to manage the balance between these styles to ensure a healthy and harmonious relationship.",
    ("avoiding", "competing", "accommodating",
     "compromising"): "Person 1's conflict resolution styles involve avoidance and competing, while Person 2 emphasizes accommodating and compromising. This mix can create a harmonious relationship where they excel in finding middle-ground solutions through accommodation and competition in both daily interactions and the life of their relationship.",
    ("avoiding", "competing", "collaborating",
     "avoiding"): "Person 1 predominantly uses avoidance and competing, while Person 2 has a prominent style of collaborating and avoiding. This dynamic may result in effective problem-solving through collaboration on certain occasions, but challenges may arise when avoidance becomes the default approach for Person 2, potentially hindering open discussions.",
    ("avoiding", "competing", "collaborating",
     "accommodating"): "Person 1 primarily uses avoidance and competing, while Person 2 prefers collaborating and accommodating. This balance between competition and accommodation can promote effective communication and cooperation in both daily interactions and the life of their relationship.",
    ("avoiding", "competing", "collaborating",
     "competing"): "In their relationship, Person 1 tends to avoid conflicts and compete, while Person 2 combines collaborating and competing. This combination can create a dynamic where they alternate between collaboration and competition in their daily interactions. While it can be stimulating, they should manage the balance to prevent potential conflicts.",
    ("avoiding", "competing", "collaborating",
     "compromising"): "Person 1's conflict resolution styles involve avoidance and competing, while Person 2 emphasizes collaborating and compromising. This mix can create a harmonious relationship where they excel in finding middle-ground solutions through collaboration in both daily interactions and the life of their relationship.",
    ("avoiding", "competing", "competing",
     "avoiding"): "Person 1 predominantly uses avoidance and competing as their conflict resolution styles, while Person 2 favors competing and avoiding. In their daily life, Person 1's competitive approach may lead to occasional tension, but Person 2's avoidance can help maintain harmony. Over time, they should find a balance between these styles to prevent conflicts from becoming more frequent.",
    ("avoiding", "competing", "competing",
     "accommodating"): "Person 1 primarily uses avoidance and competing as their conflict resolution styles, while Person 2 has the prominent styles of competing and accommodating. In their daily life, Person 1's competitive approach may lead to occasional tension, but Person 2's accommodating nature can help maintain harmony. Over time, they should find a balance between these styles to prevent conflicts from becoming more frequent.",
    ("avoiding", "competing", "competing",
     "collaborating"): "In their relationship, Person 1 tends to avoid conflicts and compete, while Person 2 combines competing and collaborating. This combination can create a dynamic where they alternate between collaboration and competition in their daily interactions. While it can be stimulating, they should manage the balance to prevent potential conflicts.",
    ("avoiding", "competing", "competing",
     "compromising"): "Person 1 primarily uses avoidance and competing, while Person 2 prefers competing and compromising. This dynamic can create a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition to dominate, leading to potential conflicts.",
    ("avoiding", "competing", "compromising",
     "avoiding"): "Person 1 predominantly uses avoidance and competing as their conflict resolution styles, while Person 2 has the prominent styles of compromising and avoiding. In their daily life, Person 1's competitive approach may lead to occasional tension, but Person 2's avoidance can help maintain harmony. Over time, they should find a balance between these styles to prevent conflicts from becoming more frequent.",
    ("avoiding", "competing", "compromising",
     "accommodating"): "Person 1 tends to avoid conflicts and compete, while Person 2 emphasizes compromising and accommodating. This mix can create a harmonious relationship where they excel in finding middle-ground solutions through accommodation and competition in both daily interactions and the life of their relationship.",
    ("avoiding", "competing", "compromising",
     "collaborating"): "Person 1's conflict resolution styles involve avoidance and competing, while Person 2 emphasizes compromising and collaborating. This mix can create a harmonious relationship where they excel in finding middle-ground solutions through collaboration in both daily interactions and the life of their relationship.",
    ("avoiding", "competing", "compromising",
     "competing"): "In their relationship, Person 1 tends to avoid conflicts and compete, while Person 2 combines compromising and competing. This dynamic can create a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition to dominate, leading to potential conflicts.",
    ("avoiding", "compromising", "accommodating",
     "avoiding"): "Person 1 primarily uses avoidance and compromising as their conflict resolution styles, while Person 2 has the prominent styles of accommodating and avoiding. In their daily life, Person 1's tendency to avoid conflicts can create temporary peace, but it may lead to unresolved issues. Person 2's accommodating nature can help maintain harmony, but they should find a balance to address underlying problems effectively.",
    ("avoiding", "compromising", "accommodating",
     "collaborating"): "In their relationship, Person 1 tends to avoid conflicts and compromise, while Person 2 emphasizes accommodating and collaborating. This mix can create a harmonious relationship where they excel in finding middle-ground solutions through collaboration and compromise in both daily interactions and the life of their relationship.",
    ("avoiding", "compromising", "accommodating",
     "competing"): "Person 1's conflict resolution styles involve avoidance and compromise, while Person 2 emphasizes accommodating and competing. This mix can create a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition to dominate, leading to potential conflicts.",
    ("avoiding", "compromising", "accommodating",
     "compromising"): "In their relationship, Person 1 tends to avoid conflicts and compromise, while Person 2 emphasizes accommodating and compromising. This combination can lead to effective conflict resolution by finding middle-ground solutions and making compromises when needed in both daily interactions and the life of their relationship.",
    ("avoiding", "compromising", "collaborating",
     "avoiding"): "Person 1 predominantly uses avoidance and compromising as their conflict resolution styles, while Person 2 has the prominent styles of collaborating and avoiding. In their daily life, Person 1's tendency to avoid conflicts can create temporary peace, but it may lead to unresolved issues. Person 2's avoidance can help maintain harmony, but they should find a balance to address underlying problems effectively.",
    ("avoiding", "compromising", "collaborating",
     "accommodating"): "In their relationship, Person 1 tends to avoid conflicts and compromise, while Person 2 emphasizes collaborating and accommodating. This mix can create a harmonious relationship where they excel in finding middle-ground solutions through collaboration and compromise in both daily interactions and the life of their relationship.",
    ("avoiding", "compromising", "collaborating",
     "competing"): "Person 1's conflict resolution styles involve avoidance and compromise, while Person 2 emphasizes collaborating and competing. This combination can lead to a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition to dominate, leading to potential conflicts.",
    ("avoiding", "compromising", "competing",
     "collaborating"): "Person 1 primarily uses avoidance and compromising as their conflict resolution styles, while Person 2 has the prominent styles of competing and collaborating. In their daily life, Person 1's tendency to avoid conflicts can create temporary peace, but it may lead to unresolved issues. Person 2's competitive nature can drive them to find solutions through collaboration, which can be beneficial if balanced properly in both daily interactions and the life of their relationship.",
    ("avoiding", "compromising", "competing",
     "compromising"): "In their relationship, Person 1 tends to avoid conflicts and compromise, while Person 2 emphasizes competing and compromising. This mix can lead to a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition and compromise to dominate, potentially leading to conflicts.",
    ("avoiding", "compromising", "compromising",
     "avoiding"): "Person 1 predominantly uses avoidance and compromising as their conflict resolution styles, while Person 2 has the prominent styles of compromising and avoiding. In their daily life, Person 1's tendency to avoid conflicts can create temporary peace, but it may lead to unresolved issues. Person 2's compromising nature can be beneficial, but they should find a balance to address underlying problems effectively in both daily interactions and the life of their relationship.",
    ("avoiding", "compromising", "compromising",
     "accommodating"): "In their relationship, Person 1 tends to avoid conflicts and compromise, while Person 2 emphasizes compromising and accommodating. This combination can lead to effective conflict resolution by finding middle-ground solutions and making compromises when needed in both daily interactions and the life of their relationship.",
    ("avoiding", "compromising", "compromising",
     "collaborating"): "Person 1's conflict resolution styles involve avoidance and compromise, while Person 2 emphasizes compromising and collaborating. This mix can create a harmonious relationship where they excel in finding middle-ground solutions and collaborating effectively in both daily interactions and the life of their relationship.",
    ("avoiding", "compromising", "compromising",
     "competing"): "Person 1 tends to avoid conflicts and compromise, while Person 2 has the prominent styles of compromising and competing. This combination can lead to a diverse range of conflict resolution strategies, which can be positive if used effectively. However, they should be mindful of not allowing competition and compromise to dominate, potentially leading to conflicts.",
    ("accommodating", "avoiding", "avoiding",
     "accommodating"): "Person 1 primarily uses accommodating and avoidance as their conflict resolution styles, while Person 2 has the prominent styles of avoiding and accommodating. In their daily life, Person 1's accommodating nature can help maintain harmony, but they should find a balance to address underlying problems effectively. Person 2's avoidance can create temporary peace, but it may lead to unresolved issues. Finding a balance is key in both daily interactions and the life of their relationship.",
    ("accommodating", "avoiding", "avoiding",
     "collaborating"): "In their relationship, Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes avoidance and collaboration. This mix can create challenges, as Person 1's accommodating nature may clash with Person 2's collaborative approach. Finding a balance between these styles is important for effective conflict resolution in both daily interactions and the life of their relationship.",
    ("accommodating", "avoiding", "avoiding",
     "competing"): "Person 1's conflict resolution styles involve accommodating and avoiding, while Person 2 has the prominent styles of avoiding and competing. This combination can lead to potential conflicts, as Person 1's accommodating nature may be at odds with Person 2's competitive approach. Finding common ground and effective communication are essential for their relationship's success.",
    ("accommodating", "avoiding", "avoiding",
     "compromising"): "In their relationship, Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes avoiding and compromising. This mix can create challenges, as Person 1's accommodating nature may clash with Person 2's compromising approach. Finding a balance between these styles is important for effective conflict resolution in both daily interactions and the life of their relationship.",
    ("accommodating", "avoiding", "accommodating",
     "collaborating"): "Person 1 primarily uses accommodating and avoiding as their conflict resolution styles, while Person 2 has the prominent styles of accommodating and collaborating. This combination can create a harmonious relationship where both prioritize accommodation and collaboration in their daily interactions. In the life of their relationship, this approach can lead to effective problem-solving and a generally positive dynamic, as long as they maintain open communication.",
    ("accommodating", "avoiding", "accommodating",
     "competing"): "In their relationship, Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes accommodation and competing. This mix can create challenges, as Person 1's accommodating nature may be at odds with Person 2's competitive approach. Finding common ground and effective communication are essential for their relationship's success.",
    ("accommodating", "avoiding", "accommodating",
     "compromising"): "Person 1 predominantly uses accommodating and avoiding as their conflict resolution styles, while Person 2 has the prominent styles of accommodating and compromising. This combination can lead to a harmonious relationship where both prioritize accommodation and compromise in their daily interactions. In the life of their relationship, this approach can lead to effective problem-solving and a generally positive dynamic, as long as they maintain open communication.",
    ("accommodating", "avoiding", "collaborating",
     "avoiding"): "Person 1 primarily uses accommodating and avoiding as their conflict resolution styles, while Person 2 has the prominent styles of collaborating and avoiding. In their daily life, Person 1's accommodating nature can help maintain harmony, but they should find a balance to address underlying problems effectively. Person 2's avoidance can create temporary peace, but it may lead to unresolved issues. Finding a balance is key in both daily interactions and the life of their relationship.",
    ("accommodating", "avoiding", "collaborating",
     "accommodating"): "In their relationship, Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes collaborating and accommodating. This combination can create a harmonious and collaborative dynamic in both daily interactions and the life of their relationship, where they prioritize accommodating each other's needs and finding mutually beneficial solutions.",
    ("accommodating", "avoiding", "collaborating",
     "competing"): "Person 1's conflict resolution styles involve accommodating and avoiding, while Person 2 has the prominent styles of collaborating and competing. This mix can create a complex but potentially effective approach to conflict resolution. They may excel in finding creative solutions through collaboration but should be mindful of how competition might impact their relationship dynamics.",
    ("accommodating", "avoiding", "collaborating",
     "compromising"): "Person 1 primarily uses accommodating and avoiding as their conflict resolution styles, while Person 2 has the prominent styles of collaborating and compromising. This combination can lead to effective conflict resolution by finding middle-ground solutions and making compromises when needed in both daily interactions and the life of their relationship.",
    ("accommodating", "avoiding", "competing",
     "avoiding"): "In their relationship, Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes competing and avoiding. This mix may create challenges, as Person 1's accommodating nature may clash with Person 2's competitive approach. Finding common ground and effective communication are essential for their relationship's success.",
    ("accommodating", "avoiding", "competing",
     "accommodating"): "Person 1 primarily uses accommodating and avoiding as their conflict resolution styles, while Person 2 has the prominent styles of competing and accommodating. This combination can create a dynamic where they prioritize accommodating each other's needs while occasionally relying on competition to drive solutions. Effective communication is key in both daily interactions and the life of their relationship.",
    ("accommodating", "avoiding", "competing",
     "collaborating"): "In their relationship, Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes competing and collaborating. This mix can create a dynamic where they rely on both competition and collaboration for conflict resolution. This can be effective if they find the right balance between these approaches and maintain open communication.",
    ("accommodating", "avoiding", "competing",
     "compromising"): "Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes competing and compromising. This mix can create a dynamic where they may struggle to find a balance between accommodating and competing, which could lead to misunderstandings and conflicts on a day-to-day basis. In the life of their relationship, success depends on their ability to effectively communicate and compromise.",
    ("accommodating", "avoiding", "compromising",
     "avoiding"): "In their relationship, Person 1 primarily uses accommodating and avoiding as their conflict resolution styles, while Person 2 has the prominent styles of compromising and avoiding. This combination may lead to a lack of direct confrontation but could also result in unresolved issues and a tendency to avoid important discussions. Open communication is crucial for addressing conflicts and maintaining a healthy relationship.",
    ("accommodating", "avoiding", "compromising",
     "accommodating"): "Person 1 predominantly uses accommodating and avoiding as their conflict resolution styles, while Person 2 has the prominent styles of compromising and accommodating. This combination can create a dynamic where they prioritize accommodating each other's needs and making compromises. In both daily interactions and the life of their relationship, this approach can lead to a harmonious and cooperative partnership.",
    ("accommodating", "avoiding", "compromising",
     "collaborating"): "Person 1 tends to accommodate and avoid conflicts, while Person 2 emphasizes compromising and collaborating. This mix can create a dynamic where they are skilled at finding middle-ground solutions and working together effectively on a day-to-day basis. In the life of their relationship, this approach can lead to successful conflict resolution and a generally positive dynamic.",
    ("accommodating", "avoiding", "compromising",
     "competing"): "In their relationship, Person 1's conflict resolution styles involve accommodating and avoiding, while Person 2 has the prominent styles of compromising and competing. This combination may lead to a complex but potentially effective approach to conflict resolution, as they balance accommodation, compromise, and competition in their interactions. Effective communication and understanding each other's preferences are key to making it work.",
    ("accommodating", "collaborating", "avoiding",
     "accommodating"): "Person 1 has prominent styles of accommodating and collaborating, while Person 2 tends to avoid conflicts and accommodate. This combination can lead to a dynamic where they prioritize accommodating each other's needs and fostering collaboration in both daily interactions and the life of their relationship. Effective communication is essential to maintain a harmonious partnership.",
    ("accommodating", "collaborating", "avoiding",
     "collaborating"): "In their relationship, Person 1 primarily uses accommodating and collaborating as their conflict resolution styles, while Person 2 has the prominent styles of avoiding and collaborating. This combination can lead to a dynamic where they prioritize collaboration and may avoid direct confrontations. In both daily interactions and the life of their relationship, success depends on their ability to address conflicts constructively when they arise.",
    ("accommodating", "collaborating", "avoiding",
     "competing"): "Person 1 tends to accommodate and collaborate, while Person 2 emphasizes avoiding and competing. This mix may lead to challenges in finding a common approach to conflict resolution. They should focus on understanding each other's styles and finding ways to integrate collaboration and competition effectively in their relationship.",
    ("accommodating", "collaborating", "avoiding",
     "compromising"): "Person 1 predominantly uses accommodating and collaborating as their conflict resolution styles, while Person 2 has the prominent styles of avoiding and compromising. This combination can lead to a dynamic where they prioritize collaboration and compromise in both daily interactions and the life of their relationship. Effective problem-solving and open communication are key to their success.",
    ("accommodating", "collaborating", "accommodating",
     "avoiding"): "In their relationship, Person 1 has prominent styles of accommodating and collaborating, while Person 2 tends to accommodate and avoid conflicts. This combination can create a harmonious dynamic where they prioritize accommodating each other's needs and fostering collaboration. In both daily interactions and the life of their relationship, open communication is essential for maintaining a positive partnership.",
    ("accommodating", "collaborating", "accommodating",
     "competing"): "Person 1 leans towards accommodating and collaborating, while Person 2 exhibits accommodating and competing as their prominent conflict resolution styles. In their daily interactions, this combination can lead to a dynamic where they prioritize cooperation and may also engage in healthy competition. In the life of their relationship, success depends on their ability to balance collaboration and competition effectively, fostering personal growth and maintaining a positive connection.",
    ("accommodating", "collaborating", "accommodating",
     "compromising"): "Person 1 tends to accommodate and collaborate, while Person 2 emphasizes accommodating and compromising. This mix creates a dynamic where they prioritize cooperation and compromise in their daily interactions. In the life of their relationship, their approach can lead to effective conflict resolution and mutual growth, provided they maintain open communication and adapt to each other's needs.",
    ("accommodating", "collaborating", "collaborating",
     "avoiding"): "In their relationship, Person 1 predominantly uses accommodating and collaborating as their conflict resolution styles, while Person 2 has the prominent styles of collaborating and avoiding. This combination can lead to a dynamic where they prioritize collaboration but may also avoid direct confrontations. In both daily interactions and the life of their relationship, success depends on their ability to address conflicts constructively when they arise and ensure that avoidance doesn't hinder communication.",
    ("accommodating", "collaborating", "collaborating",
     "accommodating"): "Person 1 leans towards accommodating and collaborating, while Person 2 exhibits collaborating and accommodating as their prominent conflict resolution styles. In their daily interactions, this combination can lead to a dynamic where they prioritize cooperation, fostering a harmonious and supportive environment. In the life of their relationship, their approach can contribute to effective conflict resolution and mutual growth.",
    ("accommodating", "collaborating", "collaborating",
     "competing"): "Person 1 predominantly uses accommodating and collaborating as their conflict resolution styles, while Person 2 has the prominent styles of collaborating and competing. This combination can create a dynamic where they prioritize collaboration but may also engage in healthy competition. In both daily interactions and the life of their relationship, success depends on their ability to balance collaboration and competition effectively, fostering personal growth and maintaining a positive connection.",
    ("accommodating", "collaborating", "collaborating",
     "compromising"): "Person 1 leans towards accommodating and collaborating, while Person 2 exhibits collaborating and compromising as their prominent conflict resolution styles. In their daily interactions, this combination can lead to a dynamic where they prioritize cooperation and compromise. In the life of their relationship, their approach can contribute to effective conflict resolution and mutual growth, provided they maintain open communication and adapt to each other's needs.",
    ("accommodating", "collaborating", "competing",
     "avoiding"): "Person 1 tends to accommodate and collaborate, while Person 2 emphasizes competing and avoiding conflicts. This mix may lead to challenges in finding a common approach to conflict resolution. They should focus on understanding each other's styles and finding ways to integrate collaboration and competition effectively in their relationship.",
    ("accommodating", "collaborating", "competing",
     "accommodating"): "Person 1 leans towards accommodating and collaborating, while Person 2 exhibits competing and accommodating as their prominent conflict resolution styles. In their daily interactions, this combination can lead to a dynamic where they prioritize cooperation while also engaging in healthy competition. In the life of their relationship, this balance can contribute to personal growth and maintaining a positive connection.",
    ("accommodating", "collaborating", "competing",
     "collaborating"): "In their relationship, Person 1 predominantly uses accommodating and collaborating as their conflict resolution styles, while Person 2 has the prominent styles of collaborating and competing. This combination can create a dynamic where they prioritize collaboration but also engage in healthy competition. In both daily interactions and the life of their relationship, success depends on their ability to balance collaboration and competition effectively, fostering personal growth and maintaining a positive connection.",
    ("accommodating", "collaborating", "competing",
     "compromising"): "Person 1 leans towards accommodating and collaborating, while Person 2 exhibits competing and compromising as their prominent conflict resolution styles. In their daily interactions, this combination can lead to a dynamic where they prioritize cooperation, engage in healthy competition, and are willing to compromise when needed. In the life of their relationship, this approach can contribute to effective conflict resolution and mutual growth, provided they maintain open communication and adapt to each other's needs.",
    ("accommodating", "collaborating", "compromising",
     "avoiding"): "Person 1 predominantly uses accommodating and collaborating as their conflict resolution styles, while Person 2 has the prominent styles of compromising and avoiding. In their daily interactions, this combination can lead to a dynamic where they prioritize cooperation and compromise but may also struggle with addressing conflicts directly. In the life of their relationship, success depends on their ability to navigate avoidance tendencies and engage in open communication when conflicts arise.",
    ("accommodating", "collaborating", "compromising",
     "accommodating"): "Person 1 leans towards accommodating and collaborating, while Person 2 exhibits compromising and accommodating as their prominent conflict resolution styles. This mix creates a dynamic where they prioritize cooperation and compromise in their daily interactions. In the life of their relationship, their approach can lead to effective conflict resolution and mutual growth, provided they maintain open communication and adapt to each other's needs.",
    ("accommodating", "collaborating", "compromising",
     "collaborating"): "In their relationship, Person 1 predominantly uses accommodating and collaborating as their conflict resolution styles, while Person 2 has the prominent styles of compromising and collaborating. This combination can create a dynamic where they prioritize cooperation and compromise, fostering a harmonious and supportive environment. In both daily interactions and the life of their relationship, their approach can contribute to effective conflict resolution and mutual growth.",
    ("accommodating", "collaborating", "compromising",
     "competing"): "Person 1 leans towards accommodating and collaborating, while Person 2 exhibits compromising and competing as their prominent conflict resolution styles. In their daily interactions, this combination can lead to a dynamic where they prioritize cooperation, engage in healthy competition, and are willing to compromise when needed. In the life of their relationship, this approach can contribute to effective conflict resolution and mutual growth, provided they maintain open communication and adapt to each other's needs.",
    ("accommodating", "competing", "avoiding",
     "accommodating"): "Person 1 tends to accommodate and compete, while Person 2 emphasizes avoiding and accommodating. This mix may create challenges in finding a common approach to conflict resolution. They should focus on understanding each other's styles and finding ways to integrate competition and cooperation effectively in their relationship.",
    ("accommodating", "competing", "avoiding",
     "collaborating"): "Person 1 leans towards accommodating and competing, while Person 2 exhibits avoiding and collaborating as their prominent conflict resolution styles. In their daily interactions, this combination can lead to a dynamic where they prioritize competition but may also struggle with addressing conflicts directly. In the life of their relationship, success depends on their ability to navigate avoidance tendencies and engage in open communication when conflicts arise.",
    ("accommodating", "competing", "avoiding",
     "competing"): "Person 1 predominantly uses accommodating and competing as their conflict resolution styles, while Person 2 has the prominent styles of avoiding and competing. This combination can lead to a dynamic where they engage in healthy competition but may also avoid direct confrontations. In both daily interactions and the life of their relationship, success depends on their ability to address conflicts constructively when they arise and ensure that avoidance doesn't hinder communication.",
    ("accommodating", "competing", "avoiding",
     "compromising"): "Person 1 leans towards accommodating and competing, while Person 2 exhibits avoiding and compromising as their prominent conflict resolution styles. In their daily interactions, this combination can create a dynamic where they prioritize competition but may also struggle with addressing conflicts directly. In the life of their relationship, success depends on their ability to navigate avoidance tendencies and engage in open communication when conflicts arise.",
    ("accommodating", "competing", "accommodating",
     "avoiding"): "Person 1 predominantly uses accommodating and competing as their conflict resolution styles, while Person 2 has the prominent styles of accommodating and avoiding. In their daily interactions, this combination can lead to a dynamic where they prioritize competition and cooperation. In the life of their relationship, their balance of accommodating and competing can contribute to personal growth and maintaining a positive connection.",
    ("accommodating", "competing", "accommodating",
     "collaborating"): "In their relationship, Person 1 leans towards accommodating and competing, while Person 2 predominantly uses accommodating and collaborating as their conflict resolution styles. This combination can create a dynamic where they engage in healthy competition and cooperation, fostering personal growth and a positive connection in both daily interactions and the life of their relationship.",
    ("Accommodating", "Competing", "Accommodating",
     "Competing"): "On the day-to-day, Person 1 tends to accommodate others, while Person 2 also has a competitive approach. This dynamic can lead to clashes when both individuals want to assert their preferences. However, in the long run, their ability to adapt and compete may balance each other out, fostering growth and healthy competition in their relationship.",
    ("Accommodating", "Competing", "Collaborating",
     "Avoiding"): "In their daily interactions, Person 1 accommodates and competes, which may result in conflicts with Person 2, who prefers collaborating and avoiding confrontation. The contrast in styles can lead to misunderstandings and tension. Over time, they may need to find a middle ground between accommodating and collaborating to maintain a harmonious relationship.",
    ("Accommodating", "Competing", "Collaborating",
     "Accommodating"): "Person 1 accommodating and competing, and Person 2 collaborating and accommodating. This mix of styles can be beneficial on a daily basis, as they balance each other's needs well. In the long run, their willingness to collaborate and adapt can create a harmonious and accommodating relationship, though they may need to address competitive tendencies when they arise.",
    ("Accommodating", "Competing", "Competing",
     "Collaborating"): "Day-to-day interactions between Person 1 (accommodating and competing) and Person 2 (competing and collaborating) may involve competition and a focus on results. While this can be productive, it might also lead to power struggles and conflicts. In the long term, their ability to combine competition and collaboration can lead to a dynamic relationship with both challenges and accomplishments.",
    ("Accommodating", "Competing", "Competing",
     "Compromising"): "On a daily basis, Person 1 accommodates and competes, while Person 2 competes and compromises. This combination can lead to conflicts as Person 1 seeks to accommodate, and Person 2 looks for compromises. In the long term, they may need to find common ground where both can accommodate and compromise effectively to maintain a balanced relationship.",
    ("Accommodating", "Competing", "Competing",
     "Avoiding"): "In their daily interactions, Person 1 tends to accommodate and compete, while Person 2 prefers competing and avoiding conflicts. This can create tension as Person 1 seeks resolution, while Person 2 avoids confrontation. In the long run, they may need to address the avoidance and find ways to balance their competing and accommodating styles for a healthier relationship.",
    ("Accommodating", "Competing", "Competing",
     "Accommodating"): "Person 1 accommodates and competes, while Person 2 competes and accommodates. This can result in a dynamic relationship with elements of competition and compromise. In the long term, their willingness to adapt and compete can create a balanced and supportive partnership.",
    ("Accommodating", "Competing", "Competing",
     "Collaborating"): "On a daily basis, Person 1 accommodates and competes, while Person 2 competes and collaborates. This combination can lead to a mixture of competitive and collaborative interactions. Over time, they may need to find ways to harmonize these styles for a more cohesive relationship.",
    ("Accommodating", "Competing", "Competing",
     "Compromising"): "Person 1 accommodating and competing, and Person 2 competing and compromising. This mix of styles can create both challenges and opportunities for their relationship. While conflicts may arise from their differences, they can also learn to balance competition and compromise to achieve mutual growth and harmony.",
    ("Accommodating", "Competing", "Compromising",
     "Avoiding"): "In their daily interactions, Person 1 accommodates and competes, while Person 2 prefers compromising and avoiding conflicts. This can lead to conflicts when Person 1 seeks resolution and Person 2 avoids confrontation. In the long run, they may need to address the avoidance and find ways to balance their styles for a more stable relationship.",
    ("Accommodating", "Competing", "Accommodating",
     "Collaborating"): "On the day-to-day, Person 1 tends to accommodate others, while Person 2 also has a competitive approach. This dynamic can lead to clashes when both individuals want to assert their preferences. However, in the long run, their ability to adapt and compete may balance each other out, fostering growth and healthy competition in their relationship.",
    ("Accommodating", "Competing", "Collaborating",
     "Avoiding"): "In their daily interactions, Person 1 accommodates and competes, which may result in conflicts with Person 2, who prefers collaborating and avoiding confrontation. The contrast in styles can lead to misunderstandings and tension. Over time, they may need to find a middle ground between accommodating and collaborating to maintain a harmonious relationship.",
    ("Accommodating", "Competing", "Collaborating",
     "Accommodating"): "Person 1 accommodating and competing, and Person 2 collaborating and accommodating. This mix of styles can be beneficial on a daily basis, as they balance each other's needs well. In the long run, their willingness to collaborate and adapt can create a harmonious and accommodating relationship, though they may need to address competitive tendencies when they arise.",
    ("Accommodating", "Competing", "Collaborating",
     "Competing"): "Day-to-day interactions between Person 1 (accommodating and competing) and Person 2 (competing and collaborating) may involve competition and a focus on results. While this can be productive, it might also lead to power struggles and conflicts. In the long term, their ability to combine competition and collaboration can lead to a dynamic relationship with both challenges and accomplishments.",
    ("Accommodating", "Competing", "Collaborating",
     "Compromising"): "On a daily basis, Person 1 accommodates and competes, while Person 2 competes and compromises. This combination can lead to conflicts as Person 1 seeks to accommodate, and Person 2 looks for compromises. In the long term, they may need to find common ground where both can accommodate and compromise effectively to maintain a balanced relationship.",
    ("Accommodating", "Competing", "Competing",
     "Avoiding"): "In their daily interactions, Person 1 tends to accommodate and compete, while Person 2 prefers competing and avoiding conflicts. This can create tension as Person 1 seeks resolution, while Person 2 avoids confrontation. In the long run, they may need to address the avoidance and find ways to balance their competing and accommodating styles for a healthier relationship.",
    ("Accommodating", "Competing", "Competing",
     "Accommodating"): "Person 1 accommodates and competes, while Person 2 competes and accommodates. This can result in a dynamic relationship with elements of competition and compromise. In the long term, their willingness to adapt and compete can create a balanced and supportive partnership.",
    ("Accommodating", "Competing", "Competing",
     "Collaborating"): "On a daily basis, Person 1 accommodates and competes, while Person 2 competes and collaborates. This combination can lead to a mixture of competitive and collaborative interactions. Over time, they may need to find ways to harmonize these styles for a more cohesive relationship.",
    ("Accommodating", "Competing", "Competing",
     "Compromising"): "Person 1 accommodating and competing, and Person 2 competing and compromising. This mix of styles can create both challenges and opportunities for their relationship. While conflicts may arise from their differences, they can also learn to balance competition and compromise to achieve mutual growth and harmony.",
    ("Accommodating", "Competing", "Compromising",
     "Avoiding"): "In their daily interactions, Person 1 accommodates and competes, while Person 2 prefers compromising and avoiding conflicts. This can lead to conflicts when Person 1 seeks resolution and Person 2 avoids confrontation. In the long run, they may need to address the avoidance and find ways to balance their styles for a more stable relationship.",
    ("Accommodating", "Competing", "Compromising",
     "Accommodating"): "Person 1 predominantly uses accommodating and competing styles, while Person 2 favors compromising and accommodating. In daily situations, their contrasting styles may lead to conflicts as Person 1 seeks to accommodate and compete, while Person 2 aims to find compromises. Over time, they can strike a balance between these styles, resulting in a relationship that combines adaptability and healthy competition.",
    ("Accommodating", "Competing", "Compromising",
     "Collaborating"): "Person 1, with accommodating and competing styles, may face challenges with Person 2, who leans towards compromising and collaborating. Daily interactions may involve negotiation and collaboration, which can be beneficial, but occasional conflicts may arise due to differences in approach. In the long run, they can develop a harmonious relationship by blending these styles effectively.",
    ("Accommodating", "Competing", "Compromising",
     "Competing"): "Person 1's accommodating and competing styles may clash with Person 2's compromising and competing tendencies in daily conflicts. They may find themselves competing for solutions, potentially leading to power struggles. Over time, they need to find ways to balance competition and compromise for a more stable relationship.",
    ("Accommodating", "Compromising", "Avoiding",
     "Accommodating"): "Person 1, who predominantly accommodates and compromises, may face challenges with Person 2, who tends to avoid conflicts and accommodate. While daily interactions may be peaceful, unresolved issues could accumulate and affect their relationship negatively. Balancing assertiveness with avoidance is crucial for long-term harmony.",
    ("Accommodating", "Compromising", "Avoiding",
     "Collaborating"): "Person 1's accommodating and compromising styles may differ from Person 2's avoidance and collaboration approach. While daily conflicts may be rare, their ability to collaborate can be an asset. Still, they should be cautious about avoiding essential discussions that can impact their relationship in the long term.",
    ("Accommodating", "Compromising", "Avoiding",
     "Competing"): "Person 1, who accommodates and compromises, may find challenges in dealing with Person 2, who tends to avoid conflicts and compete. Daily interactions may involve passive-aggressive behavior or unspoken tensions. Over time, they should work on addressing conflicts openly to maintain a healthier relationship.",
    ("Accommodating", "Compromising", "Avoiding",
     "Compromising"): "Person 1's accommodating and compromising styles may align with Person 2's avoidance and compromising tendencies. While daily interactions may be relatively conflict-free, they must ensure that important issues are not avoided entirely, as this can impact their relationship in the long term.",
    ("Accommodating", "Compromising", "Accommodating",
     "Avoiding"): "Person 1, who tends to accommodate and compromise, may encounter differences with Person 2, who accommodates and avoids conflicts. Daily life may be harmonious, but they must ensure that avoiding essential discussions doesn't lead to unresolved issues affecting their relationship negatively.",
    ("Accommodating", "Compromising", "Accommodating",
     "Collaborating"): "Person 1, with accommodating and compromising styles, may complement Person 2, who favors accommodating and collaborating. In daily interactions, they can work together effectively, combining their adaptability and willingness to collaborate for a positive and cooperative relationship.",
    ("Accommodating", "Compromising", "Accommodating",
     "Competing"): "Person 1, who accommodates and compromises, may find occasional conflicts with Person 2, who accommodates and competes. While daily life may be peaceful, they should be mindful of competitive tendencies that may arise, aiming for a balanced and supportive partnership.",
    ("Accommodating", "Compromising", "Collaborating",
     "Avoiding"): "Person 1, who predominantly uses accommodating and compromising styles, may encounter challenges with Person 2, who leans toward collaborating and avoiding conflicts. In daily situations, their differing approaches may result in conflicts, as Person 1 seeks accommodation and compromise, while Person 2 prefers collaboration and avoidance. Over time, they should find a balance between these styles for a harmonious relationship.",
    ("Accommodating", "Compromising", "Collaborating",
     "Accommodating"): "Person 1, with accommodating and compromising styles, may complement Person 2, who has collaborating and accommodating tendencies. In daily interactions, they can work together effectively, combining their adaptability and willingness to collaborate for a positive and cooperative relationship.",
    ("Accommodating", "Compromising", "Collaborating",
     "Competing"): "Person 1, who accommodates and compromises, may find occasional conflicts with Person 2, who collaborates and competes. While daily life may be peaceful, they should be mindful of competitive tendencies that may arise, aiming for a balanced and supportive partnership.",
    ("Accommodating", "Compromising", "Collaborating",
     "Compromising"): "Person 1's accommodating and compromising styles may align with Person 2's collaborating and compromising tendencies. While daily interactions may be relatively conflict-free, they must ensure that important issues are not avoided entirely, as this can impact their relationship in the long term.",
    ("Accommodating", "Compromising", "Competing",
     "Avoiding"): "In daily conflicts, Person 1, who accommodates and compromises, may face challenges dealing with Person 2, who competes and avoids confrontations. While daily life may be harmonious, they should address conflicts openly to maintain a healthier relationship.",
    ("Accommodating", "Compromising", "Competing",
     "Accommodating"): "Person 1, who predominantly accommodates and compromises, may encounter differences with Person 2, who accommodates and competes. While daily life may be peaceful, they should be cautious about competitive tendencies that may arise and aim for a balanced and supportive partnership.",
    ("Accommodating", "Compromising", "Competing",
     "Collaborating"): "In daily situations, Person 1's accommodating and compromising styles may differ from Person 2's competing and collaborating approach. While conflicts may arise from their differences, they can also learn to balance competition and compromise to achieve mutual growth and harmony.",
    ("Accommodating", "Compromising", "Competing",
     "Compromising"): "Person 1, who accommodates and compromises, may find challenges dealing with Person 2, who competes and compromises. This mix of styles can create both challenges and opportunities for their relationship. While conflicts may arise from their differences, they can also learn to balance competition and compromise to achieve mutual growth and harmony.",
    ("Accommodating", "Compromising", "Compromising",
     "Avoiding"): "Person 1, who predominantly accommodates and compromises, may face challenges with Person 2, who tends to compromise and avoid conflicts. While daily interactions may be relatively peaceful, they must ensure that important issues are not avoided entirely, as this can impact their relationship in the long term.",
    ("Accommodating", "Compromising", "Compromising",
     "Accommodating"): "Person 1, with accommodating and compromising styles, may encounter differences with Person 2, who accommodates and compromises as well. While daily life may be harmonious, they must be aware of potential conflicts that may arise due to shared accommodating and compromising tendencies and work on maintaining a healthy balance.",
    ("Accommodating", "Compromising", "Compromising",
     "Collaborating"): "Person 1, with accommodating and compromising styles, may encounter challenges with Person 2, who leans toward compromising and collaborating. In daily situations, their differing approaches may result in conflicts, as Person 1 seeks accommodation and compromise, while Person 2 prefers collaboration. Over time, they can work on finding a balance between these styles to foster a harmonious relationship.",
    ("Accommodating", "Compromising", "Compromising",
     "Competing"): "Person 1's accommodating and compromising styles may differ from Person 2's compromising and competing tendencies in daily conflicts. They may find themselves competing for solutions, potentially leading to power struggles. Over time, they need to find ways to balance competition and compromise for a more stable relationship.",
    ("Collaborating", "Avoiding", "Avoiding",
     "Accommodating"): "Person 1, who predominantly collaborates and avoids conflicts, may face challenges with Person 2, who tends to avoid conflicts and accommodate others. While daily interactions may be harmonious, they should ensure that important discussions are not avoided entirely, as this can impact their relationship in the long term.",
    ("Collaborating", "Avoiding", "Avoiding",
     "Collaborating"): "Person 1, who prefers collaborating and avoiding, may find it easier to work with Person 2, who also collaborates and avoids conflicts. This alignment in styles can lead to a peaceful daily life, but they should be cautious about avoiding crucial discussions that may affect their relationship in the long run.",
    ("Collaborating", "Avoiding", "Avoiding",
     "Competing"): "Person 1's collaborating and avoiding styles may differ from Person 2's avoiding and competitive tendencies. In daily interactions, they may find themselves facing conflicts due to their contrasting approaches. They need to find common ground and balance to maintain a healthier relationship.",
    ("Collaborating", "Avoiding", "Avoiding",
     "Compromising"): "Person 1's collaborating and avoiding styles may contrast with Person 2's avoiding and compromising tendencies. While daily interactions may be relatively conflict-free, they must ensure that important issues are not avoided entirely, as this can impact their relationship in the long term.",
    ("Collaborating", "Avoiding", "Accommodating",
     "Avoiding"): "Person 1, who collaborates and avoids conflicts, may face challenges with Person 2, who accommodates and avoids. While daily interactions may be peaceful, they should be cautious about avoiding essential discussions that can affect their relationship in the long run.",
    ("Collaborating", "Avoiding", "Accommodating",
     "Collaborating"): "Person 1's collaborating and avoiding styles may align well with Person 2's accommodating and collaborating tendencies. In daily interactions, they can work together effectively, combining their cooperative and avoiding styles for a positive and harmonious relationship.",
    ("Collaborating", "Avoiding", "Accommodating",
     "Competing"): "Person 1's collaborating and avoiding styles may differ from Person 2's accommodating and competing approaches. This contrast can lead to conflicts, but they can also find ways to balance their styles for a more harmonious relationship.",
    ("Collaborating", "Avoiding", "Accommodating",
     "Compromising"): "Person 1, with collaborating and avoiding styles, may face challenges with Person 2, who accommodates and compromises. They need to work on finding a balance between their styles to ensure a stable and mutually satisfying relationship.",
    ("Collaborating", "Avoiding", "Collaborating",
     "Accommodating"): "Person 1, with collaborating and avoiding styles, may complement Person 2, who has collaborating and accommodating tendencies. In daily interactions, they can work together effectively, combining their cooperative nature and willingness to accommodate for a positive and harmonious relationship.",
    ("Collaborating", "Avoiding", "Collaborating",
     "Competing"): "Person 1, who predominantly collaborates and avoids conflicts, may face challenges with Person 2, who also collaborates but tends to compete. Their daily interactions may involve negotiation and collaboration, which can be beneficial. However, they should be cautious about competitive tendencies that may arise, aiming for a balanced and supportive partnership.",
    ("Collaborating", "Avoiding", "Collaborating",
     "Compromising"): "Person 1's collaborating and avoiding styles may align well with Person 2's collaborating and compromising tendencies. In daily interactions, they can work together effectively, combining their cooperative styles for a harmonious relationship. Balancing compromise and collaboration will be crucial in their journey.",
    ("Collaborating", "Avoiding", "Competing",
     "Avoiding"): "Person 1, who predominantly collaborates and avoids conflicts, may find challenges with Person 2, who competes and avoids confrontations. While daily life may be harmonious, they should address conflicts openly to maintain a healthier relationship.",
    ("Collaborating", "Avoiding", "Competing",
     "Accommodating"): "Person 1, who collaborates and avoids conflicts, may encounter differences with Person 2, who competes and accommodates. While daily life may be peaceful, they should be cautious about competitive tendencies that may arise and aim for a balanced and supportive partnership.",
    ("Collaborating", "Avoiding", "Competing",
     "Collaborating"): "In daily situations, Person 1's collaborating and avoiding styles may differ from Person 2's competing and collaborating approach. While conflicts may arise from their differences, they can also learn to balance competition and compromise to achieve mutual growth and harmony.",
    ("Collaborating", "Avoiding", "Competing",
     "Compromising"): "Person 1's collaborating and avoiding styles may differ from Person 2's competing and compromising tendencies in daily conflicts. They may find themselves facing conflicts due to their contrasting approaches. They need to find common ground and balance to maintain a healthier relationship.",
    ("Collaborating", "Avoiding", "Compromising",
     "Avoiding"): "Person 1, who collaborates and avoids conflicts, may face challenges with Person 2, who compromises and avoids. While daily interactions may be harmonious, they should be cautious about avoiding essential discussions that can affect their relationship in the long run.",
    ("Collaborating", "Avoiding", "Compromising",
     "Accommodating"): "Person 1, who collaborates and avoids conflicts, may encounter differences with Person 2, who compromises and accommodates. They need to find a balance between their collaborative and accommodating tendencies to ensure a stable and mutually satisfying relationship.",
    ("Collaborating", "Avoiding", "Compromising",
     "Collaborating"): "In daily conflicts, Person 1's collaborating and avoiding styles may align well with Person 2's compromising and collaborating tendencies. They can work together effectively, combining their cooperative styles for a positive and harmonious relationship.",
    ("Collaborating", "Avoiding", "Compromising",
     "Competing"): "Person 1, with collaborating and avoiding styles, may face challenges with Person 2, who leans towards compromising and competing. Their daily interactions may involve a clash of styles, as Person 1 seeks collaboration while Person 2 may prefer competition. Finding a balance between these styles will be crucial for a successful and harmonious relationship.",
    ("Collaborating", "Accommodating", "Avoiding",
     "Accommodating"): "Person 1, who predominantly collaborates and accommodates, may have a harmonious daily life with Person 2, who avoids conflicts and also accommodates. This alignment in styles can lead to a peaceful relationship, but they should be cautious about avoiding important discussions that may affect their long-term dynamics.",
    ("Collaborating", "Accommodating", "Avoiding",
     "Collaborating"): "Person 1's collaborating and accommodating styles may align well with Person 2's avoiding and collaborating tendencies. In daily interactions, they can work together effectively, combining their cooperative nature for a positive and harmonious relationship.",
    ("Collaborating", "Accommodating", "Avoiding",
     "Competing"): "Person 1, with collaborating and accommodating styles, may encounter differences with Person 2, who avoids conflicts and tends to compete. While daily life may be peaceful, they should be cautious about competitive tendencies that may arise and aim for a balanced and supportive partnership.",
    ("Collaborating", "Accommodating", "Avoiding",
     "Compromising"): "Person 1's collaborating and accommodating styles may differ from Person 2's avoiding and compromising tendencies in daily conflicts. They may find themselves facing conflicts due to their contrasting approaches. They need to find common ground and balance to maintain a healthier relationship.",
    ("Collaborating", "Accommodating", "Accommodating",
     "Avoiding"): "Person 1, who collaborates and accommodates, may face challenges with Person 2, who accommodates and avoids conflicts. While daily interactions may be harmonious, they should be cautious about avoiding important discussions that can impact their relationship in the long run.",
    ("Collaborating", "Accommodating", "Accommodating",
     "Collaborating"): "Person 1's collaborating and accommodating styles may align well with Person 2's accommodating and collaborating tendencies. In daily interactions, they can work together effectively, combining their cooperative nature for a positive and harmonious relationship.",
    ("Collaborating", "Accommodating", "Accommodating",
     "Competing"): "Person 1, with collaborating and accommodating styles, may have differences with Person 2, who also accommodates but tends to compete. While daily life may be peaceful, they should be cautious about competitive tendencies that may arise and aim for a balanced and supportive partnership.",
    ("Collaborating", "Accommodating", "Accommodating",
     "Compromising"): "Person 1's collaborating and accommodating styles may differ from Person 2's accommodating and compromising tendencies in daily conflicts. They may find themselves facing conflicts due to their contrasting approaches. They need to find common ground and balance to maintain a healthier relationship.",
    ("Collaborating", "Accommodating", "Collaborating",
     "Avoiding"): "Person 1's collaborating and accommodating styles may differ from Person 2's collaborating and avoiding approaches in daily conflicts. While they may collaborate well, they should be cautious about avoiding important discussions that can impact their relationship in the long run.",
    ("Collaborating", "Accommodating", "Collaborating",
     "Competing"): "Person 1, with collaborating and accommodating styles, may have a dynamic relationship with Person 2, who prefers collaborating and competing. On some days, their shared collaboration can lead to successful outcomes, while on others, competing tendencies might create tension. Overall, their relationship can be a mix of productivity and competition, requiring effective communication.",
    ("Collaborating", "Accommodating", "Collaborating",
     "Compromising"): "Person 1, with collaborating and accommodating styles, may have a balanced relationship with Person 2, who also values collaboration and compromising. Their daily interactions may involve constructive compromises, contributing to a harmonious and productive partnership.",
    ("Collaborating", "Accommodating", "Competing",
     "Avoiding"): "Person 1, with collaborating and accommodating styles, may face challenges with Person 2, who tends to compete and avoid conflicts. Some days, they may excel in collaboration, but others might involve avoidance and competition, impacting the consistency of their relationship.",
    ("Collaborating", "Accommodating", "Competing",
     "Accommodating"): "Person 1's collaborating and accommodating styles can complement Person 2's competing and accommodating tendencies in their relationship. Their daily interactions may involve a blend of collaboration and compromise, contributing to a harmonious partnership.",
    ("Collaborating", "Accommodating", "Competing",
     "Collaborating"): "Person 1, with collaborating and accommodating styles, may have a dynamic relationship with Person 2, who prefers collaborating and competing. On some days, their shared collaboration can lead to successful outcomes, while on others, competing tendencies might create tension. Overall, their relationship can be a mix of productivity and competition, requiring effective communication.",
    ("Collaborating", "Accommodating", "Competing",
     "Compromising"): "Person 1, with collaborating and accommodating styles, may find differences with Person 2, who prefers competing and compromising. While some days may involve productive compromises, others might see competitive challenges. Maintaining a balanced approach will be crucial for a successful relationship.",
    ("Collaborating", "Accommodating", "Compromising",
     "Avoiding"): "Person 1, with collaborating and accommodating styles, may face challenges with Person 2, who tends to compromise and avoid conflicts. While some days may involve effective compromise, others might lead to avoidance, impacting the consistency of their relationship.",
    ("Collaborating", "Accommodating", "Compromising",
     "Accommodating"): "Person 1's collaborating and accommodating styles can complement Person 2's compromising and accommodating tendencies in their relationship. Their daily interactions may involve a balance of compromise and cooperation, contributing to a harmonious partnership.",
    ("Collaborating", "Accommodating", "Compromising",
     "Collaborating"): "Person 1, with collaborating and accommodating styles, may find similarities with Person 2, who values collaborating and compromising. Their daily interactions may involve productive compromises, contributing to a harmonious and balanced partnership.",
    ("Collaborating", "Accommodating", "Compromising",
     "Competing"): "Person 1, with collaborating and accommodating styles, may have differences with Person 2, who prefers compromising and competing. While some days may involve effective compromise, others might see competitive challenges. Maintaining a balanced approach will be crucial for a successful relationship.",
    ("Collaborating", "Competing", "Avoiding",
     "Accommodating"): "Person 1, with collaborating and competing styles, may experience some challenges in their relationship with Person 2, who prefers avoiding and accommodating. On certain days, their collaboration and competition can lead to positive outcomes. However, the presence of avoidance and accommodation might hinder their ability to address conflicts effectively.",
    ("Collaborating", "Competing", "Avoiding",
     "Collaborating"): "Person 1, with collaborating and competing styles, may have a dynamic relationship with Person 2, who values collaborating and avoiding. Their collaboration can lead to productive results on some days, but the presence of avoidance may create occasional setbacks. Overall, their relationship may involve a mix of cooperation and avoidance, depending on the circumstances.",
    ("Collaborating", "Competing", "Avoiding",
     "Competing"): "Person 1, with collaborating and competing styles, may have a competitive relationship with Person 2, who also prefers competing. While their competitive nature can drive them to achieve, the presence of avoidance may lead to missed opportunities for effective conflict resolution.",
    ("Collaborating", "Competing", "Avoiding",
     "Compromising"): "Person 1, with collaborating and competing styles, may face challenges with Person 2, who tends to avoid conflicts and compromise when necessary. Their competing tendencies can lead to moments of tension, while the presence of compromising may help ease some conflicts.",
    ("Collaborating", "Competing", "Accommodating",
     "Avoiding"): "Person 1, with collaborating and competing styles, may find it challenging to balance their approach in a relationship with Person 2, who values accommodating and avoiding. Their daily interactions may involve a mix of collaboration, competition, accommodation, and occasional avoidance.",
    ("Collaborating", "Competing", "Accommodating",
     "Collaborating"): "Person 1, with collaborating and competing styles, may have a dynamic relationship with Person 2, who prefers collaborating and accommodating. On some days, their shared collaboration can lead to successful outcomes, while on others, competing tendencies might create tension. Overall, their relationship can be a mix of productivity and competition, requiring effective communication.",
    ("Collaborating", "Competing", "Accommodating",
     "Competing"): "Person 1, with collaborating and competing styles, may have a competitive relationship with Person 2, who also prefers competing. While their competitive nature can drive them to achieve, the presence of accommodation may influence the dynamics of their relationship.",
    ("Collaborating", "Competing", "Accommodating",
     "Compromising"): "Person 1, with collaborating and competing styles, may face challenges with Person 2, who tends to accommodate and compromise when necessary. Their competing tendencies can lead to moments of tension, while the presence of compromising may help ease some conflicts.",
    ("Collaborating", "Competing", "Collaborating",
     "Avoiding"): "Person 1, with collaborating and competing styles, may have a dynamic relationship with Person 2, who prefers collaborating and avoiding. On some days, their shared collaboration can lead to successful outcomes, while on others, competing tendencies might create tension. Overall, their relationship can be a mix of productivity and competition, requiring effective communication.",
    ("Collaborating", "Competing", "Collaborating",
     "Accommodating"): "Person 1, with collaborating and competing styles, may have a dynamic relationship with Person 2, who prefers collaborating and accommodating. On some days, their shared collaboration can lead to successful outcomes, while on others, competing tendencies might create tension. Overall, their relationship can be a mix of productivity and competition, requiring effective communication.",
    ("Collaborating", "Competing", "Collaborating",
     "Compromising"): "Person 1, with collaborating and competing styles, may have a dynamic relationship with Person 2, who values collaborating and compromising. On certain days, their shared collaboration can lead to productive results, while Person 2's compromising style may contribute to effective conflict resolution. Overall, their relationship may involve a mix of cooperation and compromise, creating a good balance.",
    ("Collaborating", "Competing", "Competing",
     "Avoiding"): "Person 1, with collaborating and competing styles, may experience challenges in their relationship with Person 2, who prefers competing and avoiding. Their competitive nature might lead to occasional tension, and the presence of avoidance could hinder addressing conflicts effectively.",
    ("Collaborating", "Competing", "Competing",
     "Accommodating"): "Person 1, with collaborating and competing styles, may have a competitive relationship with Person 2, who values competing and accommodating. While their competitive tendencies can drive them to achieve, the presence of accommodation may influence the dynamics of their relationship.",
    ("Collaborating", "Competing", "Competing",
     "Collaborating"): "Person 1, with collaborating and competing styles, may have a dynamic relationship with Person 2, who prefers competing and collaborating. On some days, their shared collaboration can lead to successful outcomes, while on others, competing tendencies might create tension. Overall, their relationship can be a mix of productivity and competition, requiring effective communication.",
    ("Collaborating", "Competing", "Competing",
     "Compromising"): "Person 1, with collaborating and competing styles, may have a competitive relationship with Person 2, who tends to compromise when conflicts arise. While their competing tendencies can lead to moments of tension, the presence of compromising may help ease some conflicts.",
    ("Collaborating", "Competing", "Compromising", "Avoiding"): "Person 1, with collaborating and competing styles, may experience challenges with Person 2, who prefers compromising and avoiding. Their competing tendencies can lead to moments of tension, while the presence of avoidance may create occasional setbacks in addressing conflicts.",
    ("Collaborating", "Competing", "Compromising",
     "Accommodating"): "Person 1, with collaborating and competing styles, may face challenges with Person 2, who values compromising and accommodating. Their competing tendencies can lead to moments of tension, while the presence of accommodating and compromising may contribute to effective conflict resolution.",
    ("Collaborating", "Competing", "Compromising",
     "Collaborating"): "Person 1, with collaborating and competing styles, may have a dynamic relationship with Person 2, who prefers compromising and collaborating. On some days, their shared collaboration can lead to successful outcomes, while on others, competing tendencies might create tension. Overall, their relationship can be a mix of productivity and competition, requiring effective communication.",
    ("Collaborating", "Competing", "Compromising",
     "Competing"): "Person 1, with collaborating and competing styles, may have a competitive relationship with Person 2, who also prefers competing. While their competitive nature can drive them to achieve, the presence of compromising and accommodating may influence the dynamics of their relationship.",
    ("Collaborating", "Compromising", "Avoiding",
     "Accommodating"): "Person 1, with collaborating and compromising styles, may have a complex relationship with Person 2, who values avoiding and accommodating. On certain days, their compromise and accommodation can lead to effective conflict resolution, but the presence of avoidance may create occasional setbacks in addressing conflicts.",
    ("Collaborating", "Compromising", "Avoiding",
     "Collaborating"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values collaborating and avoiding. Their collaborative approach can lead to effective conflict resolution, while Person 2's avoidance style might pose occasional challenges. Overall, their relationship may involve productive collaboration but may also require addressing avoidance tendencies.",
    ("Collaborating", "Compromising", "Avoiding",
     "Competing"): "Person 1, with collaborating and compromising styles, may face challenges in their relationship with Person 2, who prefers avoiding and competing. Their collaborative tendencies can lead to effective resolution, but Person 2's competitive style may create occasional tensions and conflicts.",
    ("Collaborating", "Compromising", "Avoiding",
     "Compromising"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values collaborating and compromising. Their ability to collaborate and compromise can lead to effective conflict resolution. Overall, their relationship may involve productive collaboration and negotiation.",
    ("Collaborating", "Compromising", "Accommodating",
     "Avoiding"): "Person 1, with collaborating and compromising styles, may face challenges in their relationship with Person 2, who prefers accommodating and avoiding. While their collaborative and compromising tendencies can contribute to resolution, Person 2's avoidance style may hinder addressing conflicts effectively.",
    ("Collaborating", "Compromising", "Accommodating",
     "Collaborating"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values collaborating and accommodating. Their collaborative approach can lead to effective conflict resolution, and Person 2's accommodating style may facilitate smooth interactions. Overall, their relationship may involve productive collaboration and accommodation.",
    ("Collaborating", "Compromising", "Accommodating",
     "Competing"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who prefers accommodating and competing. Their collaborative tendencies can lead to effective resolution, while Person 2's competitive style may create occasional tensions and challenges.",
    ("Collaborating", "Compromising", "Accommodating",
     "Compromising"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values collaborating and compromising. Their ability to collaborate and compromise can lead to effective conflict resolution. Overall, their relationship may involve productive collaboration and negotiation.",
    ("Collaborating", "Compromising", "Collaborating",
     "Avoiding"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who prefers collaborating and avoiding. Their collaborative approach can lead to effective conflict resolution, while Person 2's avoidance style may create occasional challenges. Overall, their relationship may involve productive collaboration but may also require addressing avoidance tendencies.",
    ("Collaborating", "Compromising", "Collaborating",
     "Accommodating"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values collaborating and accommodating. Their collaborative approach can lead to effective conflict resolution, and Person 2's accommodating style may facilitate smooth interactions. Overall, their relationship may involve productive collaboration and accommodation.",
    ("Collaborating", "Compromising", "Collaborating",
     "Competing"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who prefers collaborating and competing. Their collaborative tendencies can lead to effective resolution, while Person 2's competitive style may create occasional tensions and challenges.",
    ("Collaborating", "Compromising", "Competing",
     "Avoiding"): "Person 1, with collaborating and compromising styles, may face challenges in their relationship with Person 2, who prefers competing and avoiding. While their collaborative and compromising tendencies can contribute to resolution, Person 2's competitive style may create occasional tensions and conflicts.",
    ("Collaborating", "Compromising", "Competing",
     "Accommodating"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values competing and accommodating. Their collaborative tendencies can lead to effective resolution, while Person 2's accommodating style may facilitate smooth interactions. Overall, their relationship may involve productive collaboration and accommodation.",
    ("Collaborating", "Compromising", "Competing",
     "Collaborating"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who prefers competing and collaborating. Their collaborative approach can lead to effective conflict resolution, and Person 2's collaborative style may complement their efforts. Overall, their relationship may involve productive collaboration and cooperation.",
    ("Collaborating", "Compromising", "Competing",
     "Compromising"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values competing and compromising. Their ability to collaborate and compromise can lead to effective conflict resolution. Overall, their relationship may involve productive collaboration and negotiation.",
    ("Collaborating", "Compromising", "Compromising",
     "Avoiding"): "Person 1, with collaborating and compromising styles, may face challenges in their relationship with Person 2, who prefers compromising and avoiding. While their collaborative and compromising tendencies can contribute to resolution, Person 2's avoidance style may hinder addressing conflicts effectively.",
    ("Collaborating", "Compromising", "Compromising",
     "Accommodating"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values compromising and accommodating. Their collaborative approach can lead to effective conflict resolution, and Person 2's accommodating style may facilitate smooth interactions. Overall, their relationship may involve productive collaboration and accommodation.",
    ("Collaborating", "Compromising", "Compromising",
     "Collaborating"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who prefers compromising and collaborating. Their collaborative approach can lead to effective conflict resolution, and Person 2's collaborative style may complement their efforts. Overall, their relationship may involve productive collaboration and cooperation.",
    ("Collaborating", "Compromising", "Compromising",
     "Competing"): "Person 1, with collaborating and compromising styles, may have a balanced relationship with Person 2, who values compromising and competing. Their ability to collaborate and compromise can lead to effective conflict resolution. Overall, their relationship may involve productive collaboration and negotiation.",
    ("Competing", "Avoiding", "Avoiding",
     "Accommodating"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who prefers avoiding and accommodating. Their competitive tendencies may lead to conflicts, and Person 2's accommodating style may help manage these conflicts. Overall, their relationship may involve occasional tensions but can benefit from accommodation.",
    ("Competing", "Avoiding", "Avoiding",
     "Collaborating"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who values avoiding and collaborating. Their competitive tendencies may lead to conflicts, and Person 2's collaborative style may help address these conflicts effectively. Overall, their relationship may involve occasional tensions but can benefit from collaboration.",
    ("Competing", "Avoiding", "Avoiding",
     "Competing"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who values avoiding and competing. While their competitive tendencies can lead to conflicts, their shared inclination toward competition may create a lively dynamic, both on a day-to-day basis and in the long term.",
    ("Competing", "Avoiding", "Avoiding",
     "Compromising"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who prefers avoiding and compromising. Their competitive tendencies may lead to conflicts, and Person 2's compromising style may help manage these conflicts. Overall, their relationship may involve occasional tensions but can benefit from compromise.",
    ("Competing", "Avoiding", "Accommodating",
     "Avoiding"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who values accommodating and avoiding. Their competitive tendencies may lead to conflicts, and Person 2's avoidance style may hinder addressing conflicts effectively.",
    ("Competing", "Avoiding", "Accommodating",
     "Collaborating"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who prefers accommodating and collaborating. While their competitive tendencies can lead to conflicts, Person 2's collaborative style may help address these conflicts effectively. Overall, their relationship may involve occasional tensions but can benefit from collaboration.",
    ("Competing", "Avoiding", "Accommodating",
     "Competing"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who values accommodating and competing. While their competitive tendencies can lead to conflicts, their shared inclination toward competition may create a lively dynamic, both on a day-to-day basis and in the long term.",
    ("Competing", "Avoiding", "Accommodating",
     "Compromising"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who prefers accommodating and compromising. Their competitive tendencies may lead to conflicts, and Person 2's compromising style may help manage these conflicts. Overall, their relationship may involve occasional tensions but can benefit from compromise.",
    ("Competing", "Avoiding", "Collaborating",
     "Avoiding"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who values collaborating and avoiding. While their competitive tendencies can lead to conflicts, Person 2's avoidance style may hinder addressing conflicts effectively.",
    ("Competing", "Avoiding", "Collaborating",
     "Accommodating"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who prefers collaborating and accommodating. While their competitive tendencies can lead to conflicts, Person 2's accommodating style may facilitate smoother interactions. Overall, their relationship may involve occasional tensions but can benefit from accommodation.",
    ("Competing", "Avoiding", "Collaborating",
     "Competing"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who values collaborating and competing. While their competitive tendencies can lead to conflicts, their shared inclination toward competition may create a lively dynamic, both on a day-to-day basis and in the long term.",
    ("Competing", "Avoiding", "Collaborating",
     "Compromising"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who prefers collaborating and compromising. Their competitive tendencies may lead to conflicts, and Person 2's compromising style may help manage these conflicts. Overall, their relationship may involve occasional tensions but can benefit from compromise.",
    ("Competing", "Avoiding", "Competing",
     "Accommodating"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who values competing and accommodating. While their competitive tendencies can lead to conflicts, Person 2's accommodating style may help alleviate tensions and foster a cooperative environment. Overall, their relationship may have its ups and downs but can benefit from accommodation.",
    ("Competing", "Avoiding", "Competing",
     "Collaborating"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who prefers competing and collaborating. While their competitive tendencies can lead to conflicts, Person 2's collaborative style may help address these conflicts effectively. Overall, their relationship may involve occasional tensions but can benefit from collaboration.",
    ("Competing", "Avoiding", "Competing",
     "Compromising"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who values competing and compromising. Their competitive tendencies may lead to conflicts, and Person 2's compromising style may help manage these conflicts. Overall, their relationship may involve occasional tensions but can benefit from compromise.",
    ("Competing", "Avoiding", "Compromising",
     "Avoiding"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who prefers compromising and avoiding. Their competitive tendencies may lead to conflicts, and Person 2's avoidance style may hinder addressing conflicts effectively.",
    ("Competing", "Avoiding", "Compromising",
     "Accommodating"): "Person 1, with competing and avoiding styles, may have a challenging relationship with Person 2, who values compromising and accommodating. Their competitive tendencies may lead to conflicts, and Person 2's accommodating style may help manage these conflicts. Overall, their relationship may involve occasional tensions but can benefit from accommodation.",
    ("Competing", "Avoiding", "Compromising",
     "Collaborating"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who prefers compromising and collaborating. While their competitive tendencies can lead to conflicts, Person 2's collaborative style may help address these conflicts effectively. Overall, their relationship may involve occasional tensions but can benefit from collaboration.",
    ("Competing", "Avoiding", "Compromising",
     "Competing"): "Person 1, with competing and avoiding styles, may have a dynamic relationship with Person 2, who values compromising and competing. While their competitive tendencies can lead to conflicts, their shared inclination toward competition may create a lively dynamic, both on a day-to-day basis and in the long term.",
    ("Competing", "Accommodating", "Avoiding",
     "Accommodating"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values avoiding and accommodating. Their accommodating tendencies may help maintain a harmonious environment, but occasional conflicts stemming from Person 1's competitiveness and Person 2's avoidance may arise. Overall, their relationship may have a positive tone with occasional challenges.",
    ("Competing", "Accommodating", "Avoiding",
     "Collaborating"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who prefers avoiding and collaborating. While their accommodating tendencies may help maintain a harmonious environment, conflicts stemming from Person 1's competitiveness and Person 2's avoidance may require effective collaboration to resolve. Overall, their relationship may have a positive tone with occasional challenges.",
    ("Competing", "Accommodating", "Avoiding",
     "Competing"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values avoiding and competing. Their accommodating tendencies may help maintain a harmonious environment, but occasional conflicts stemming from Person 1's competitiveness and Person 2's competitive nature may arise. Overall, their relationship may have a positive tone with occasional challenges.",
    ("Competing", "Accommodating", "Avoiding",
     "Compromising"): "Person 1, with competing and accommodating styles, may have a balanced approach to conflicts. Person 2, with avoiding and compromising styles, can complement this balance. Their relationship benefits from effective compromise and problem-solving, leading to a generally positive and harmonious dynamic in both daily interactions and the long term.",
    ("Competing", "Accommodating", "Accommodating",
     "Avoiding"): "Person 1, with competing and accommodating styles, may find themselves in a relationship with Person 2, who also leans toward accommodating but occasionally avoids conflicts. While their accommodation can foster a pleasant atmosphere, Person 2's avoidance may lead to unaddressed issues over time, causing some challenges in the relationship.",
    ("Competing", "Accommodating", "Accommodating",
     "Collaborating"): "Person 1, with competing and accommodating styles, may find themselves in a relationship with Person 2, who values both accommodation and collaboration. Their shared willingness to accommodate and collaborate can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Accommodating", "Accommodating",
     "Competing"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who also values competing and occasionally accommodating. Their shared competitiveness may lead to occasional conflicts, but their willingness to accommodate can help mitigate tensions. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Accommodating", "Accommodating",
     "Compromising"): "Person 1, with competing and accommodating styles, may have a balanced approach to conflicts. Person 2, with accommodating and compromising styles, can complement this balance. Their relationship benefits from effective compromise and problem-solving, leading to a generally positive and harmonious dynamic in both daily interactions and the long term.",
    ("Competing", "Accommodating", "Collaborating",
     "Avoiding"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values collaborating and avoiding conflicts. While their collaborative tendencies can foster problem-solving, Person 2's avoidance may lead to unresolved issues over time, causing occasional challenges in their relationship.",
    ("Competing", "Accommodating", "Collaborating",
     "Accommodating"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values both collaboration and accommodation. Their shared willingness to collaborate and accommodate can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Accommodating", "Collaborating",
     "Competing"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who also values competing and occasionally collaborating. Their shared competitiveness may lead to occasional conflicts, but their willingness to collaborate can help mitigate tensions. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Accommodating", "Collaborating",
     "Compromising"): "Person 1, with competing and accommodating styles, may have a balanced approach to conflicts. Person 2, with collaborating and compromising styles, can complement this balance. Their relationship benefits from effective compromise and problem-solving, leading to a generally positive and harmonious dynamic in both daily interactions and the long term.",
    ("Competing", "Accommodating", "Competing",
     "Avoiding"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values both competing and avoiding conflicts. Their shared competitiveness may lead to occasional conflicts, and Person 2's avoidance may hinder addressing these conflicts effectively, causing challenges in their relationship.",
    ("Competing", "Accommodating", "Competing",
     "Collaborating"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values both competing and collaborating. Their shared competitiveness may lead to occasional conflicts, but their willingness to collaborate can help mitigate tensions. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Accommodating", "Competing",
     "Compromising"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values both competing and compromising. Their shared competitiveness may lead to occasional conflicts, but their willingness to compromise can help them find common ground. Overall, their relationship may involve a mix of competition and compromise, with both daily and long-term implications.",
    ("Competing", "Accommodating", "Compromising",
     "Avoiding"): "Person 1, with competing and accommodating styles, may find themselves in a challenging relationship with Person 2, who values compromising but occasionally avoids conflicts. While Person 1 is willing to accommodate, Person 2's avoidance may hinder effective conflict resolution, leading to unresolved issues over time.",
    ("Competing", "Accommodating", "Compromising",
     "Accommodating"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values both compromising and accommodating. Their shared willingness to compromise and accommodate can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Accommodating", "Compromising",
     "Collaborating"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who values both compromising and collaborating. Their shared willingness to compromise and collaborate can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Accommodating", "Compromising",
     "Competing"): "Person 1, with competing and accommodating styles, may have a dynamic relationship with Person 2, who also values competing and occasionally compromises. Their shared competitiveness may lead to occasional conflicts, but their willingness to compromise can help them find common ground. Overall, their relationship may involve a mix of competition and compromise, with both daily and long-term implications.",
    ("Competing", "Collaborating", "Avoiding",
     "Accommodating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values both avoiding conflicts and accommodating. While their collaboration fosters problem-solving, Person 2's avoidance may occasionally hinder addressing conflicts effectively, causing occasional challenges in their relationship.",
    ("Competing", "Collaborating", "Avoiding",
     "Collaborating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values both avoiding conflicts and collaborating. Their collaboration fosters problem-solving and a cooperative atmosphere, leading to positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Avoiding",
     "Competing"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who also values competing and collaborating. Their shared competitiveness may lead to occasional conflicts, but their collaborative tendencies can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Collaborating", "Avoiding",
     "Compromising"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values both avoiding conflicts and compromising. While their collaboration fosters problem-solving, Person 2's avoidance may occasionally hinder addressing conflicts effectively, causing occasional challenges in their relationship.",
    ("Competing", "Collaborating", "Accommodating",
     "Avoiding"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values accommodating and avoiding conflicts. While their collaboration can lead to effective problem-solving, Person 2's avoidance tendencies may occasionally hinder addressing conflicts. Their relationship may involve a balance between constructive collaboration and challenges arising from avoidance.",
    ("Competing", "Collaborating", "Accommodating",
     "Collaborating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who also values collaborating and accommodating. Their shared willingness to collaborate and accommodate can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Accommodating",
     "Competing"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who also values competing and collaborating. Their shared competitiveness may lead to occasional conflicts, but their collaborative tendencies can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Collaborating", "Accommodating",
     "Compromising"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values collaborating and compromising. Their shared willingness to collaborate and compromise can create a balanced and effective approach to conflict resolution, leading to positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Collaborating",
     "Avoiding"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values collaborating and occasionally avoids conflicts. While their collaboration fosters effective problem-solving, Person 2's avoidance tendencies may lead to occasional challenges in addressing conflicts, impacting their relationship.",
    ("Competing", "Collaborating", "Collaborating",
     "Accommodating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values both collaborating and accommodating. Their shared willingness to collaborate and accommodate can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Collaborating",
     "Competing"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who also values competing and collaborating. Their shared competitiveness may lead to occasional conflicts, but their collaborative tendencies can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Collaborating", "Collaborating",
     "Compromising"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values collaborating and compromising. Their shared willingness to collaborate and compromise can create a balanced and effective approach to conflict resolution, leading to positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Competing",
     "Avoiding"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values competing and occasionally avoids conflicts. Their collaboration can lead to effective problem-solving, but Person 2's avoidance tendencies may occasionally hinder addressing conflicts. Their relationship may involve a balance between collaboration and challenges arising from avoidance.",
    ("Competing", "Collaborating", "Competing",
     "Accommodating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values both competing and accommodating. Their shared competitiveness may lead to occasional conflicts, but their willingness to accommodate can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Collaborating", "Competing",
     "Compromising"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values competing and compromising. Their shared competitiveness may lead to occasional conflicts, but their willingness to compromise can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Collaborating", "Compromising",
     "Avoiding"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values compromising and occasionally avoids conflicts. While their collaboration can lead to effective problem-solving, Person 2's avoidance tendencies may occasionally hinder addressing conflicts, impacting their relationship.",
    ("Competing", "Collaborating", "Compromising",
     "Accommodating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values compromising and accommodating. Their shared willingness to collaborate and accommodate can create a balanced and effective approach to conflict resolution, leading to positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Compromising",
     "Collaborating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values compromising and collaborating. Their shared willingness to collaborate and compromise can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Compromising",
     "Competing"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who also values competing and collaborating. Their shared competitiveness may lead to occasional conflicts, but their collaborative tendencies can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Compromising", "Avoiding",
     "Accommodating"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values avoiding and accommodating. Their competitiveness and Person 2's avoidance tendencies may create challenges in addressing conflicts, affecting their relationship.",
    ("Competing", "Compromising", "Avoiding",
     "Collaborating"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values avoiding and collaborating. While their willingness to compromise can be beneficial, Person 2's avoidance tendencies may occasionally hinder addressing conflicts, impacting their relationship.",
    ("Competing", "Compromising", "Avoiding",
     "Competing"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who also values competing and compromising. Their shared competitiveness may lead to occasional conflicts, but their willingness to compromise can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Compromising", "Avoiding",
     "Compromising"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values avoiding and compromising. Their willingness to compromise and find middle ground can be a strength in addressing conflicts, contributing to a positive relationship.",
    ("Competing", "Compromising", "Accommodating",
     "Avoiding"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values accommodating and avoiding. Their willingness to compromise and accommodate can be beneficial, but Person 2's avoidance tendencies may occasionally hinder addressing conflicts, affecting their relationship.",
    ("Competing", "Collaborating", "Competing",
     "Compromising"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values competing and compromising. Their shared competitiveness may lead to occasional conflicts, but their willingness to compromise can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Collaborating", "Compromising",
     "Avoiding"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values compromising and occasionally avoids conflicts. While their collaboration can lead to effective problem-solving, Person 2's avoidance tendencies may occasionally hinder addressing conflicts, impacting their relationship.",
    ("Competing", "Collaborating", "Compromising",
     "Accommodating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values compromising and accommodating. Their shared willingness to collaborate and accommodate can create a balanced and effective approach to conflict resolution, leading to positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Compromising",
     "Collaborating"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who values compromising and collaborating. Their shared willingness to collaborate and compromise can create a harmonious and cooperative relationship, fostering positive daily interactions and long-term dynamics.",
    ("Competing", "Collaborating", "Compromising",
     "Competing"): "Person 1, with competing and collaborating styles, may have a dynamic relationship with Person 2, who also values competing and collaborating. Their shared competitiveness may lead to occasional conflicts, but their collaborative tendencies can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Compromising", "Avoiding",
     "Accommodating"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values avoiding and accommodating. Their competitiveness and Person 2's avoidance tendencies may create challenges in addressing conflicts, affecting their relationship.",
    ("Competing", "Compromising", "Avoiding",
     "Collaborating"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values avoiding and collaborating. While their willingness to compromise can be beneficial, Person 2's avoidance tendencies may occasionally hinder addressing conflicts, impacting their relationship.",
    ("Competing", "Compromising", "Avoiding",
     "Competing"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who also values competing and compromising. Their shared competitiveness may lead to occasional conflicts, but their willingness to compromise can help them find common ground. Overall, their relationship may involve a mix of competition and cooperation, with both daily and long-term implications.",
    ("Competing", "Compromising", "Avoiding",
     "Compromising"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values avoiding and compromising. Their willingness to compromise and find middle ground can be a strength in addressing conflicts, contributing to a positive relationship.",
    ("Competing", "Compromising", "Accommodating",
     "Avoiding"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values accommodating and avoiding. Their willingness to compromise and accommodate can be beneficial, but Person 2's avoidance tendencies may occasionally hinder addressing conflicts, affecting their relationship.",
    ("Competing", "Compromising", "Competing",
     "Avoiding"): "Person 1, with competing and compromising styles, may face challenges in their relationship with Person 2, who values competing and avoiding conflicts. The frequent clash between their competing styles and Person 2's avoidance tendencies can lead to daily conflicts and strain their long-term relationship.",
    ("Competing", "Compromising", "Competing",
     "Accommodating"): "Person 1, with competing and compromising styles, may experience a dynamic relationship with Person 2, who values competing and accommodating. While their competitiveness may lead to daily conflicts, their willingness to accommodate and compromise can contribute positively to their long-term relationship.",
    ("Competing", "Compromising", "Competing",
     "Collaborating"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values competing and collaborating. Their shared competitiveness may lead to daily conflicts, but their collaborative tendencies and occasional compromise can create a balanced dynamic in their long-term relationship.",
    ("Competing", "Compromising", "Compromising",
     "Avoiding"): "Person 1, with competing and compromising styles, may face challenges in their relationship with Person 2, who values compromising and avoiding conflicts. The frequent clash between their conflicting styles can lead to daily conflicts, affecting the long-term health of their relationship.",
    ("Competing", "Compromising", "Compromising",
     "Accommodating"): "Person 1, with competing and compromising styles, may experience a dynamic relationship with Person 2, who values compromising and accommodating. Their willingness to accommodate and compromise can contribute positively to their long-term relationship, even though daily conflicts may arise.",
    ("Competing", "Compromising", "Compromising",
     "Collaborating"): "Person 1, with competing and compromising styles, may have a dynamic relationship with Person 2, who values compromising and collaborating. Their willingness to compromise and collaborate can create a balanced dynamic in their long-term relationship, despite occasional daily conflicts.",
    ("Competing", "Compromising", "Compromising",
     "Competing"): "Person 1, with competing and compromising styles, may experience a dynamic relationship with Person 2, who also values competing and compromising. Their shared competitiveness may lead to daily conflicts, but their willingness to compromise can help them find common ground in their long-term relationship.",
    ("Compromising", "Avoiding", "Avoiding",
     "Accommodating"): "Person 1, with compromising and avoiding styles, may face challenges in their relationship with Person 2, who values avoiding and accommodating. The lack of conflict resolution strategies may result in daily misunderstandings and, over time, strain their relationship.",
    ("Compromising", "Avoiding", "Avoiding",
     "Collaborating"): "Person 1, with compromising and avoiding styles, may have a dynamic relationship with Person 2, who values avoiding and collaborating. Their frequent avoidance tendencies may lead to daily misunderstandings, affecting their long-term relationship.",
    ("Compromising", "Avoiding", "Avoiding",
     "Competing"): "Person 1, with compromising and avoiding styles, may face challenges in their relationship with Person 2, who values avoiding and competing. The lack of common ground in conflict resolution may lead to daily conflicts and strain their long-term relationship.",
    ("Compromising", "Avoiding", "Avoiding",
     "Compromising"): "Person 1, with compromising and avoiding styles, may find common ground with Person 2, who values avoiding and compromising. Their shared willingness to compromise and avoid unnecessary conflicts can contribute positively to their daily interactions and long-term relationship.",
    ("Compromising", "Avoiding", "Accommodating",
     "Avoiding"): "Person 1, with compromising and avoiding styles, may face challenges in their relationship with Person 2, who values accommodating and avoiding conflicts. The frequent clash between their conflict resolution styles may lead to daily challenges, impacting the overall quality of their long-term relationship.",
    ("Compromising", "Avoiding", "Accommodating",
     "Collaborating"): "Person 1, with compromising and avoiding styles, may experience a dynamic relationship with Person 2, who values accommodating and collaborating. While their avoidance tendencies can create daily challenges, their willingness to accommodate and collaborate may positively impact their long-term relationship.",
    ("Compromising", "Avoiding", "Accommodating",
     "Competing"): "Person 1, with compromising and avoiding styles, may have a dynamic relationship with Person 2, who values accommodating and competing. The conflict between their avoidance and competitiveness may lead to daily challenges, but their willingness to accommodate can contribute positively to their long-term relationship.",
    ("Compromising", "Avoiding", "Accommodating",
     "Compromising"): "Person 1, with compromising and avoiding styles, may find compatibility with Person 2, who values accommodating and compromising. Their shared willingness to compromise and accommodate can contribute positively to their daily interactions and long-term relationship.",
    ("Compromising", "Avoiding", "Collaborating",
     "Avoiding"): "Person 1, with compromising and avoiding styles, may face challenges in their relationship with Person 2, who values collaborating and avoiding. The frequent clash between their conflict resolution styles may lead to daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Avoiding", "Collaborating",
     "Accommodating"): "Person 1, with compromising and avoiding styles, may experience a dynamic relationship with Person 2, who values collaborating and accommodating. While their avoidance tendencies can create daily challenges, their willingness to accommodate and collaborate may positively impact their long-term relationship.",
    ("Compromising", "Avoiding", "Collaborating",
     "Competing"): "Person 1, with compromising and avoiding styles, may have a dynamic relationship with Person 2, who values collaborating and competing. The conflict between their avoidance and competitiveness may lead to daily challenges, but their willingness to collaborate can contribute positively to their long-term relationship.",
    ("Compromising", "Avoiding", "Collaborating",
     "Compromising"): "Person 1, with compromising and avoiding styles, may find compatibility with Person 2, who values collaborating and compromising. Their shared willingness to compromise and collaborate can contribute positively to their daily interactions and long-term relationship.",
    ("Compromising", "Avoiding", "Competing",
     "Avoiding"): "Person 1, with compromising and avoiding styles, may face challenges in their relationship with Person 2, who values competing and avoiding conflicts. The frequent clash between their conflict resolution styles may lead to daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Avoiding", "Competing",
     "Accommodating"): "Person 1, with compromising and avoiding styles, may face challenges in their relationship with Person 2, who values competing and accommodating. The frequent clash between their conflict resolution styles may lead to daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Avoiding", "Competing",
     "Collaborating"): "Person 1, with compromising and avoiding styles, may experience a dynamic relationship with Person 2, who values competing and collaborating. The conflict between their avoidance and competitiveness may lead to daily challenges, but their willingness to collaborate can contribute positively to their long-term relationship.",
    ("Compromising", "Avoiding", "Competing",
     "Compromising"): "Person 1, with compromising and avoiding styles, may find compatibility with Person 2, who values competing and compromising. Their shared willingness to compromise and accommodate can contribute positively to their daily interactions and long-term relationship.",
    ("Compromising", "Avoiding", "Compromising",
     "Accommodating"): "Person 1, with compromising and avoiding styles, may experience a dynamic relationship with Person 2, who values compromising and accommodating. While their avoidance tendencies can create daily challenges, their willingness to accommodate and compromise may positively impact their long-term relationship.",
    ("Compromising", "Avoiding", "Compromising",
     "Collaborating"): "Person 1, with compromising and avoiding styles, may find compatibility with Person 2, who values compromising and collaborating. Their shared willingness to compromise and collaborate can contribute positively to their daily interactions and long-term relationship.",
    ("Compromising", "Avoiding", "Compromising",
     "Competing"): "Person 1, with compromising and avoiding styles, may have a dynamic relationship with Person 2, who values compromising and competing. The conflict between their avoidance and competitiveness may lead to daily challenges, but their willingness to compromise can contribute positively to their long-term relationship.",
    ("Compromising", "Accommodating", "Avoiding",
     "Accommodating"): "Person 1, with compromising and accommodating styles, may find common ground with Person 2, who values avoiding and accommodating. Their shared willingness to accommodate and avoid unnecessary conflicts can contribute positively to their daily interactions and long-term relationship.",
    ("Compromising", "Accommodating", "Avoiding",
     "Collaborating"): "Person 1, with compromising and accommodating styles, may face challenges in their relationship with Person 2, who values avoiding and collaborating. The frequent clash between their conflict resolution styles may lead to daily challenges, impacting the overall quality of their long-term relationship.",
    ("Compromising", "Accommodating", "Avoiding",
     "Competing"): "Person 1, with compromising and accommodating styles, may have a dynamic relationship with Person 2, who values avoiding and competing. The conflict between their avoidance and competitiveness may lead to daily challenges, but their willingness to accommodate can contribute positively to their long-term relationship.",
    ("Compromising", "Accommodating", "Avoiding",
     "Compromising"): "Person 1, with compromising and accommodating styles, may find compatibility with Person 2, who values avoiding and compromising. Their shared willingness to compromise and accommodate can contribute positively to their daily interactions and long-term relationship.",
    ("Compromising", "Accommodating", "Accommodating",
     "Avoiding"): "Person 1, with compromising and accommodating styles, may have a relatively smooth daily interaction with Person 2, who values accommodating and avoiding. Their shared willingness to accommodate and avoid conflicts can contribute positively to their day-to-day interactions, leading to a relatively good relationship. However, their avoidance of certain issues may lead to unresolved tensions over time.",
    ("Compromising", "Accommodating", "Accommodating",
     "Collaborating"): "Person 1, with compromising and accommodating styles, may have a harmonious daily interaction with Person 2, who values accommodating and collaborating. Their shared willingness to accommodate and collaborate can contribute positively to their daily interactions, fostering a good long-term relationship.",
    ("Compromising", "Accommodating", "Accommodating",
     "Competing"): "Person 1, with compromising and accommodating styles, may experience occasional conflicts with Person 2, who values accommodating and competing. The clash between their accommodating and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Accommodating", "Accommodating",
     "Compromising"): "Person 1, with compromising and accommodating styles, may have a relatively good daily interaction with Person 2, who values accommodating and compromising. Their shared willingness to compromise and accommodate can contribute positively to their day-to-day interactions, leading to a good long-term relationship with effective conflict resolution.",
    ("Compromising", "Accommodating", "Collaborating",
     "Avoiding"): "Person 1, with compromising and accommodating styles, may face challenges in their relationship with Person 2, who values collaborating and avoiding. The frequent clash between their conflict resolution styles may lead to daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Accommodating", "Collaborating",
     "Accommodating"): "Person 1, with compromising and accommodating styles, may have a harmonious daily interaction with Person 2, who values collaborating and accommodating. Their shared willingness to accommodate and collaborate can contribute positively to their daily interactions, fostering a good long-term relationship.",
    ("Compromising", "Accommodating", "Collaborating",
     "Competing"): "Person 1, with compromising and accommodating styles, may experience occasional conflicts with Person 2, who values collaborating and competing. The clash between their collaborative and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Accommodating", "Collaborating",
     "Compromising"): "Person 1, with compromising and accommodating styles, may have a relatively good daily interaction with Person 2, who values collaborating and compromising. Their shared willingness to compromise and accommodate can contribute positively to their day-to-day interactions, leading to a good long-term relationship with effective conflict resolution.",
    ("Compromising", "Accommodating", "Competing",
     "Avoiding"): "Person 1, with compromising and accommodating styles, may experience occasional conflicts with Person 2, who values competing and avoiding. The clash between their accommodating and competitive styles may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Accommodating", "Competing",
     "Accommodating"): "Person 1, with compromising and accommodating styles, may have a harmonious daily interaction with Person 2, who values competing and accommodating. Their shared willingness to accommodate can contribute positively to their daily interactions, fostering a good long-term relationship.",
    ("Compromising", "Accommodating", "Competing",
     "Collaborating"): "Person 1, with compromising and accommodating styles, may experience a balanced daily interaction with Person 2, who values competing and collaborating. Their ability to compromise and accommodate, along with collaboration, can contribute positively to their day-to-day interactions, leading to a good and harmonious long-term relationship.",
    ("Compromising", "Accommodating", "Competing",
     "Compromising"): "Person 1, with compromising and accommodating styles, may face occasional conflicts with Person 2, who values competing and compromising. The clash between their compromising and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Accommodating", "Compromising",
     "Avoiding"): "Person 1, with compromising and accommodating styles, may experience daily challenges in their relationship with Person 2, who values compromising and avoiding. The frequent clash between their compromising and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Accommodating", "Compromising",
     "Collaborating"): "Person 1, with compromising and accommodating styles, may have a relatively good daily interaction with Person 2, who values compromising and collaborating. Their shared willingness to compromise and collaborate can contribute positively to their day-to-day interactions, leading to a good long-term relationship with effective conflict resolution.",
    ("Compromising", "Accommodating", "Compromising",
     "Competing"): "Person 1, with compromising and accommodating styles, may face occasional conflicts with Person 2, who values compromising and competing. The clash between their compromising and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Avoiding",
     "Accommodating"): "Person 1, with compromising and collaborating styles, may face challenges in their relationship with Person 2, who values avoiding and accommodating. The frequent clash between their collaborating and accommodating tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Avoiding",
     "Collaborating"): "Person 1, with compromising and collaborating styles, may have a harmonious daily interaction with Person 2, who values avoiding and collaborating. Their shared willingness to collaborate can contribute positively to their day-to-day interactions, fostering a good long-term relationship.",
    ("Compromising", "Collaborating", "Avoiding",
     "Competing"): "Person 1, with compromising and collaborating styles, may experience occasional conflicts with Person 2, who values avoiding and competing. The clash between their collaborating and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Avoiding",
     "Compromising"): "Person 1, with compromising and collaborating styles, may experience a balanced daily interaction with Person 2, who values avoiding and compromising. Their ability to compromise and collaborate, along with compromising, can contribute positively to their day-to-day interactions, leading to a good and harmonious long-term relationship.",
    ("Compromising", "Collaborating", "Accommodating",
     "Avoiding"): "Person 1, with compromising and collaborating styles, may face challenges in their relationship with Person 2, who values accommodating and avoiding. The frequent clash between their collaborating and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Accommodating",
     "Collaborating"): "Person 1, with compromising and collaborating styles, may have a harmonious daily interaction with Person 2, who values accommodating and collaborating. Their shared willingness to collaborate can contribute positively to their day-to-day interactions, fostering a good long-term relationship.",
    ("Compromising", "Collaborating", "Accommodating",
     "Competing"): "Person 1, with compromising and collaborating styles, may experience occasional conflicts with Person 2, who values accommodating and competing. The clash between their collaborating and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Accommodating",
     "Compromising"): "Person 1, with compromising and collaborating styles, may experience a balanced daily interaction with Person 2, who values accommodating and compromising. Their ability to compromise and collaborate, along with compromising, can contribute positively to their day-to-day interactions, leading to a good and harmonious long-term relationship.",
    ("Compromising", "Collaborating", "Collaborating",
     "Avoiding"): "Person 1, with compromising and collaborating styles, may face challenges in their relationship with Person 2, who values collaborating and avoiding. The frequent clash between their collaborating and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Collaborating",
     "Accommodating"): "Person 1, with compromising and collaborating styles, may have a harmonious daily interaction with Person 2, who values collaborating and accommodating. Their shared willingness to collaborate can contribute positively to their day-to-day interactions, fostering a good long-term relationship.",
    ("Compromising", "Collaborating", "Collaborating",
     "Competing"): "Person 1, with compromising and collaborating styles, may experience occasional conflicts with Person 2, who values collaborating and competing. The clash between their collaborating and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Collaborating",
     "Compromising"): "Person 1, with compromising and collaborating styles, may experience a balanced daily interaction with Person 2, who values collaborating and compromising. Their ability to compromise and collaborate, along with compromising, can contribute positively to their day-to-day interactions, leading to a good and harmonious long-term relationship.",
    ("Compromising", "Collaborating", "Competing",
     "Avoiding"): "Person 1, with compromising and collaborating styles, may face challenges in their relationship with Person 2, who values competing and avoiding. The frequent clash between their collaborating and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Competing",
     "Accommodating"): "Person 1, with compromising and collaborating styles, may experience occasional conflicts with Person 2, who values competing and accommodating. The clash between their collaborating and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Competing",
     "Collaborating"): "Person 1, with compromising and collaborating styles, may have a harmonious daily interaction with Person 2, who values competing and collaborating. Their shared willingness to collaborate can contribute positively to their day-to-day interactions, fostering a good long-term relationship.",
    ("Compromising", "Collaborating", "Competing",
     "Compromising"): "Person 1, with compromising and collaborating styles, may experience a balanced daily interaction with Person 2, who values competing and compromising. Their ability to compromise and collaborate, along with compromising, can contribute positively to their day-to-day interactions, leading to a good and harmonious long-term relationship.",
    ("Compromising", "Collaborating", "Compromising",
     "Avoiding"): "Person 1, with compromising and collaborating styles, may face challenges in their relationship with Person 2, who values compromising and avoiding. The frequent clash between their compromising and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Collaborating", "Compromising",
     "Accommodating"): "Person 1, with compromising and collaborating styles, may have a harmonious daily interaction with Person 2, who values compromising and accommodating. Their shared willingness to compromise can contribute positively to their day-to-day interactions, fostering a good long-term relationship.",
    ("Compromising", "Collaborating", "Compromising",
     "Competing"): "Person 1, with compromising and collaborating styles, may experience occasional conflicts with Person 2, who values compromising and competing. The clash between their compromising and competitive tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Avoiding",
     "Accommodating"): "Person 1, with compromising and competing styles, may face challenges in their relationship with Person 2, who values avoiding and accommodating. The frequent clash between their competing and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Avoiding",
     "Collaborating"): "Person 1, with compromising and competing styles, may experience occasional conflicts with Person 2, who values avoiding and collaborating. The clash between their competing and collaborative tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Avoiding",
     "Competing"): "Person 1, with compromising and competing styles, may face challenges in their relationship with Person 2, who values competing and avoiding. The frequent clash between their competing and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Avoiding",
     "Compromising"): "Person 1, with compromising and competing styles, may experience occasional conflicts with Person 2, who values avoiding and compromising. The clash between their competing and compromising tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Accommodating",
     "Avoiding"): "Person 1, with compromising and competing styles, may face challenges in their relationship with Person 2, who values accommodating and avoiding. The frequent clash between their competing and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Accommodating",
     "Collaborating"): "Person 1, with compromising and competing styles, may have a harmonious daily interaction with Person 2, who values accommodating and collaborating. Their shared willingness to collaborate can contribute positively to their day-to-day interactions, fostering a good long-term relationship.",
    ("Compromising", "Competing", "Accommodating",
     "Competing"): "Person 1, with compromising and competing styles, may experience a mix of daily interactions with Person 2, who values accommodating and competing. Their ability to compete and their shared willingness to accommodate can contribute positively to some aspects of their day-to-day interactions, but may also lead to occasional conflicts due to competitive tendencies, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Accommodating",
     "Compromising"): "Person 1, with compromising and competing styles, may have a balanced daily interaction with Person 2, who values accommodating and compromising. Their ability to compromise and their shared willingness to accommodate can contribute positively to their day-to-day interactions, leading to a good and harmonious long-term relationship.",
    ("Compromising", "Competing", "Collaborating",
     "Avoiding"): "Person 1, with compromising and competing styles, may face challenges in their relationship with Person 2, who values collaborating and avoiding. The clash between their competitive and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Collaborating",
     "Accommodating"): "Person 1, with compromising and competing styles, may experience occasional conflicts with Person 2, who values collaborating and accommodating. The clash between their competitive and accommodating tendencies may lead to some daily challenges, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Collaborating",
     "Competing"): "Person 1, with compromising and competing styles, may have a competitive daily interaction with Person 2, who values collaborating and competing. Their shared competitive tendencies may contribute to a competitive atmosphere in their day-to-day interactions, which can be both good and not so good for their long-term relationship.",
    ("Compromising", "Competing", "Collaborating",
     "Compromising"): "Person 1, with compromising and competing styles, may experience a mix of daily interactions with Person 2, who values collaborating and compromising. Their ability to compromise and their shared willingness to collaborate can contribute positively to some aspects of their day-to-day interactions, but may also lead to occasional conflicts due to competitive tendencies, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Competing",
     "Avoiding"): "Person 1, with compromising and competing styles, may face challenges in their relationship with Person 2, who values competing and avoiding. The frequent clash between their competitive and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Competing",
     "Accommodating"): "Person 1, with compromising and competing styles, may have a competitive daily interaction with Person 2, who values competing and accommodating. Their shared competitive tendencies may contribute to a competitive atmosphere in their day-to-day interactions, which can be both good and not so good for their long-term relationship.",
    ("Compromising", "Competing", "Competing",
     "Collaborating"): "Person 1, with compromising and competing styles, may have a competitive daily interaction with Person 2, who values competing and collaborating. Their shared competitive tendencies may contribute to a competitive atmosphere in their day-to-day interactions, which can be both good and not so good for their long-term relationship.",
    ("Compromising", "Competing", "Competing",
     "Compromising"): "Person 1, with compromising and competing styles, may experience a mix of daily interactions with Person 2, who values competing and compromising. Their ability to compromise and their shared competitive tendencies may lead to a balanced daily interaction, but occasional conflicts due to competitive tendencies can affect the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Compromising",
     "Avoiding"): "Person 1, with compromising and competing styles, may have a challenging daily interaction with Person 2, who values compromising and avoiding. Their frequent clashes between competitive and avoiding tendencies may lead to unresolved conflicts, affecting the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Compromising",
     "Accommodating"): "Person 1, with compromising and competing styles, may experience a mix of daily interactions with Person 2, who values compromising and accommodating. Their ability to compromise and their shared competitive tendencies may lead to a balanced daily interaction, but occasional conflicts due to competitive tendencies can affect the overall quality of their long-term relationship.",
    ("Compromising", "Competing", "Compromising",
     "Collaborating"): "Person 1, with compromising and competing styles, may have a competitive daily interaction with Person 2, who values compromising and collaborating. Their shared competitive tendencies may contribute to a competitive atmosphere in their day-to-day interactions, which can be both good and not so good for their long-term relationship.",
}


def multiple_equals(val, target):
    return [i for i, v in enumerate(val) if str(v) == str(target)]


def reanalyze(json_data, style_data):
    print("\nReanalyzing conflict resolution style...")

    values = json_data.get('the_values', [])
    max_style = json_data.get('the_max', 'Unknown')
    secondaries = json_data.get('the_secondaries', 'Unknown')
    least_styles = json_data.get('the_leasts', 'Unknown')

    print(f"Name: {json_data.get('name', 'Unknown')}")
    print(f"Main Style: {max_style}")
    print(f"Secondary Styles: {secondaries}")
    print(f"Least Styles: {least_styles}")

    save_bar_chart(json_data.get('name', 'Unknown'), values, save=False)

    while True:
        try:
            reanalysis_choice = input("Do you want to save a new analysis? (yes/no): ").strip().lower()
            if reanalysis_choice == 'yes':
                analyze()
                break
            elif reanalysis_choice == 'no':
                print("Exiting reanalysis.")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        except ValueError:
            print("Invalid input. Please enter 'yes' or 'no'.")


def save_bar_chart(name, values, save=True):
    if not os.path.exists("bargraphs"):
        os.makedirs("bargraphs")

    filename = f"bargraphs/{name.replace(' ', '_')}_{date.today()}.png"

    colors = ['blue' if value == max(values) else 'green' if value == sorted(values)[-2] else 'red' if value == min(
        values) else 'gray' for value in values]

    plt.figure(figsize=(10, 6))
    plt.barh(["accommodating", "avoiding", "collaborating", "competing", "compromising"], values, color=colors)
    plt.xlabel('Count')
    plt.title(f'Conflict Resolution Style for {name}')

    legend_labels = ['blue most', 'green secondary', 'red least', 'grey unrated']
    legend_colors = ['blue', '#00b050', 'red', 'gray']
    legend_patches = [Patch(color=color, label=label) for color, label in zip(legend_colors, legend_labels)]

    plt.legend(title='Color Code', labels=legend_labels, handles=legend_patches, bbox_to_anchor=(1.04, 0.5), loc='best',
               borderaxespad=0, fontsize=12, frameon=False, facecolor='white')

    plt.tight_layout()

    if save:
        plt.savefig(filename)

    plt.show()


def save_data_to_file(name, values, styles):
    if not os.path.exists("testdata"):
        os.makedirs("testdata")

    filename = f"testdata/conflictresolutiondb.txt"

    with open(filename, "a") as file:
        data = f"{name}, {', '.join(styles)}, '{', '.join(map(str, values))}'\n"
        file.write(data)


def find_sec_largest(lst):
    sorted_lst = sorted(lst)
    return sorted_lst[-2]


def analyze():
    cls()
    print("You selected 'Analyze'.")

    def get_answers():
        answers = []
        questions = [
            "1. I explore issues with others to find solutions that meet everyone's needs",
            "2. I try to negotiate and adopt a 'give-and-take' approach to problem situations",
            "3. I try to meet the expectations of others.",
            "4. I generally argue my case and insist on the merits of my point of view.",
            "5. When there is a disagreement, I gather as much information as I can to keep the lines of communication open.",
            "6. When I find myself in an argument, I usually say very little and try to leave as soon as possible.",
            "7. I try to see conflicts from both sides. What do I need? What does the other person need? What are the issues involved?",
            "8. I prefer to compromise when solving problems and just move on.",
            "9. I find conflicts challenging and exhilarating. I enjoy the battle of wits that usually follows.",
            "10. Being at odds with other people makes me feel uncomfortable and anxious.",
            "11. I try to accommodate the wishes of my friends and family.",
            "12. I can figure out what needs to be done and I am usually right.",
            "13. To break deadlocks, I would meet people halfway.",
            "14. I may not get what I want, but it is a small price to pay for keeping the peace.",
            "15. I avoid hard feelings by keeping my disagreements with others to myself."
        ]

        for i, question in enumerate(questions, start=1):
            while True:
                cls()
                ans = input(
                    f"{question}\nAnswer: 1, 2, 3, 4 (1 rarely, 2 sometimes, 3 often, 4 always, or type 'exit' to quit): ")
                if ans == 'exit':
                    return answers
                if ans in ['1', '2', '3', '4']:
                    answers.append(ans)
                    break
                else:
                    print("Please answer with 1, 2, 3, or 4, or type 'exit' to quit.")
        return answers

    name = input("What is your name: ")
    print(f"Hello {name}, let's test your conflict resolution style")
    print("I will ask you 15 questions.")

    answers = get_answers()
    if not answers:
        return  # User chose to exit

    collaborating_cnt = sum(int(ans) for i, ans in enumerate(answers, start=1) if i in [1, 5, 7])
    competing_cnt = sum(int(ans) for i, ans in enumerate(answers, start=1) if i in [4, 9, 12])
    avoiding_cnt = sum(int(ans) for i, ans in enumerate(answers, start=1) if i in [6, 10, 15])
    accommodating_cnt = sum(int(ans) for i, ans in enumerate(answers, start=1) if i in [3, 11, 14])
    compromising_cnt = sum(int(ans) for i, ans in enumerate(answers, start=1) if i in [2, 8, 13])

    values = [accommodating_cnt, avoiding_cnt, collaborating_cnt, competing_cnt, compromising_cnt]

    max_value = max(values)
    max_indices = multiple_equals(values, max_value)

    second_largest = find_sec_largest(values)
    second_indices = multiple_equals(values, second_largest)

    min_value = min(values)
    min_indices = multiple_equals(values, min_value)

    styles = ["accommodating", "avoiding", "collaborating", "competing", "compromising"]
    style_data = [styles[i] for i in max_indices]

    cls()
    print(f"You are mostly {', '.join(style_data)} ({max_value})")
    cls()
    print(f"Hello, {name}, you are mostly {', '.join(style_data)} ({max_value})")

    if len(second_indices) > 1:
        print("Your secondary styles are equally:", ', '.join([styles[i] for i in second_indices]),
              f"({second_largest})")
    else:
        print(f"Your secondary style is {styles[second_indices[0]]} ({second_largest})")

    if len(min_indices) > 1:
        print("Your least styles are equally:", ', '.join([styles[i] for i in min_indices]), f"({min_value})")
    else:
        print(f"Your least conflict resolution style is {styles[min_indices[0]]} ({min_value})")

    save_bar_chart(name, values)
    save_data_to_file(name, values, style_data)

    json_data = {
        "name": name,
        "style_data": style_data,
        "the_values": values,
        "the_max": ', '.join(style_data),
        "the_secondaries": ', '.join([styles[i] for i in second_indices]),
        "the_leasts": ', '.join([styles[i] for i in min_indices])
    }

    json_filename = f"conflictjsons/{name}_conflict_data.json"

    with open(json_filename, "w") as json_file:
        json.dump(json_data, json_file, indent=2)


def retrieve():
    print("You selected 'Retrieve'.")

    name_prefix = input("Enter the first 3 letters of the name: ").strip().lower()
    file_list = glob.glob(f"conflictjsons/{name_prefix}*.json")

    if not file_list:
        print("No matching files found.")
        return

    print("Matching files:")
    for i, file_path in enumerate(file_list, start=1):
        print(f"{i}: {file_path}")

    while True:
        try:
            selection = int(input(f"Select a file by entering its number (1-{len(file_list)}): "))
            if 1 <= selection <= len(file_list):
                break
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    selected_file_path = file_list[selection - 1]

    with open(selected_file_path, 'r') as file:
        json_data = json.load(file)
        print("Contents of selected JSON file:")
        print(json.dumps(json_data, indent=4))

        style_data = json_data.get('style_data', [])
        name = json_data.get('name', 'Unknown')

        print("Values from 'style_data' key:", style_data)

        reanalyze(json_data, style_data)


def browse():
    cls()
    print("You selected 'Browse'.")

    start_index = 0  # Initialize the starting index
    while True:
        # List 8 names at a time starting from the current start_index
        file_list = glob.glob("conflictjsons/*.json")
        if not file_list or start_index >= len(file_list):
            print("No more names to browse.")
            return

        names_to_display = file_list[start_index:start_index + 8]
        print("Names in this group:")
        for i, file_path in enumerate(names_to_display, start=1):
            print(f"{i}: {os.path.splitext(os.path.basename(file_path))[0]}")
        print("9: Next")
        print("10: Exit Browse")

        while True:
            try:
                selection = int(
                    input(f"Select a name by entering its number (1-8), '9' for Next, or '10' to exit browse: "))
                if 1 <= selection <= 8:
                    selected_file_path = names_to_display[selection - 1]
                    with open(selected_file_path, 'r') as file:
                        json_data = json.load(file)
                        print("Contents of selected JSON file:")
                        print(json.dumps(json_data, indent=4))
                        style_data = json_data.get('style_data', [])
                        name = json_data.get('name', 'Unknown')
                        print("Values from 'style_data' key:", style_data)
                        reanalyze(json_data, style_data)
                        break
                elif selection == 9:
                    cls()
                    start_index += 8  # Move to the next group of 8 names
                    break
                elif selection == 10:
                    print("Exiting Browse.")
                    return
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


splash = "|||||||*****************************|||||||\n"
splash += "Welcome to the Conflict Compatibility Compass - This is a Conflict Resolution Style Analysis tool "
splash += "with top 2 style comparison functionality\n"
splash += "|||||||*****************************|||||||\n"

wrapped_splash = textwrap.fill(splash, width=50)

print(wrapped_splash)


while True:
    print("Menu:")
    print("1. Analyze")
    print("2. Retrieve")
    print("3. Browse")
    print("4. Compare")
    print("5. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        cls()
        analyze()
    elif choice == '2':
        cls()
        retrieve()
    elif choice == '3':
        cls()
        browse()
    elif choice == '4':
        cls()
        compare()
    elif choice == '5' or choice.lower() == 'exit':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option (1/2/3/4).")
