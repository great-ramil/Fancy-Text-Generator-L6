import telebot, os
from telebot import types
import generator

def board(current_i, total, style):
    buttons = types.InlineKeyboardMarkup()
    name = types.InlineKeyboardButton(style, callback_data='name')
    previous = types.InlineKeyboardButton('<', callback_data='prev')
    next = types.InlineKeyboardButton('>', callback_data='next')
    current = types.InlineKeyboardButton(f"{current_i}/{total}", callback_data='current')
    pick = types.InlineKeyboardButton('Готово', callback_data='pick')
    buttons.add(name)
    buttons.add(previous, current, next)
    buttons.add(pick)
    return buttons

def preview(style):
    preview = generator.generate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', style)
    return preview