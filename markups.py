from telebot import types

stats_menu = types.InlineKeyboardMarkup(row_width=1)
item_number_of_students = types.InlineKeyboardButton(text='Number of students', callback_data='number_students')
item_number_of_unknown_faces = types.InlineKeyboardButton(text='Number of unknown faces registered',
                                                          callback_data='number_unknowns')
item_unknown_faces = types.InlineKeyboardButton(text="List of unknown faces", callback_data="unknown_faces")
stats_menu.add(item_number_of_students, item_number_of_unknown_faces, item_unknown_faces)

confirm_add_student = types.InlineKeyboardMarkup(row_width=2)
item_yes = types.InlineKeyboardButton(text="Yes", callback_data='yes')
item_no = types.InlineKeyboardButton(text="No", callback_data='no')
confirm_add_student.add(item_yes, item_no)

settings_menu = types.InlineKeyboardMarkup(row_width=1)
item_tolerance = types.InlineKeyboardButton(text="tolerance", callback_data='change_tolerance')
settings_menu.add(item_tolerance)

tolerance_menu = types.InlineKeyboardMarkup(row_width=3)
item_1 = types.InlineKeyboardButton(text='0.1', callback_data='0.1')
item_2 = types.InlineKeyboardButton(text='0.2', callback_data='0.2')
item_3 = types.InlineKeyboardButton(text='0.3', callback_data='0.3')
item_4 = types.InlineKeyboardButton(text='0.4', callback_data='0.4')
item_5 = types.InlineKeyboardButton(text='0.5', callback_data='0.5')
item_6 = types.InlineKeyboardButton(text='0.6', callback_data='0.6')
item_7 = types.InlineKeyboardButton(text='0.7', callback_data='0.7')
item_8 = types.InlineKeyboardButton(text='0.8', callback_data='0.8')
item_9 = types.InlineKeyboardButton(text='0.9', callback_data='0.9')
tolerance_menu.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8, item_9)



