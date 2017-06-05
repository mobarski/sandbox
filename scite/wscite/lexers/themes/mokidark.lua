-- Copyright 2006-2017 Mitchell mitchell.att.foicica.com. See LICENSE.
-- SciTE lexer theme for Scintillua.

local property = require('lexer').property

property['color.red'] = '#F92672'
property['color.yellow'] = '#E6DB74'
property['color.black'] = '#F8F8F2'
property['color.white'] = '#272822'
property['color.green'] = '#A6E22E'
property['color.orange'] = '#FD971F'
property['color.blue'] = '#66D9EF'
property['color.purple'] = '#AE81FF'
property['color.grey'] = '#75715E'
property['color.teal'] = '#AE81FF'

-- Default style.
-- local font, size = 'Verdana', 9
local font, size = 'Consolas', 9
property['style.default'] = 'font:'..font..',size:'..size..
                            ',fore:$(color.black),back:$(color.white)'

-- Token styles.
property['style.nothing'] = ''
property['style.class'] = 'fore:$(color.black),bold'
property['style.comment'] = 'fore:$(color.grey)'
property['style.constant'] = 'fore:$(color.teal),bold'
property['style.definition'] = 'fore:$(color.black),bold'
property['style.error'] = 'fore:$(color.red)'
property['style.function'] = 'fore:$(color.black),bold'
property['style.keyword'] = 'fore:$(color.blue),bold'
property['style.label'] = 'fore:$(color.teal),bold'
property['style.number'] = 'fore:$(color.teal)'
property['style.operator'] = 'fore:$(color.black),bold'
property['style.regex'] = '$(style.string)'
property['style.string'] = 'fore:$(color.yellow)'
property['style.preprocessor'] = 'fore:$(color.yellow)'
property['style.tag'] = 'fore:$(color.teal)'
property['style.type'] = 'fore:$(color.blue)'
property['style.variable'] = 'fore:$(color.black)'
property['style.whitespace'] = ''
property['style.embedded'] = 'fore:$(color.blue)'
property['style.identifier'] = '$(style.nothing)'

-- Predefined styles.
property['style.linenumber'] = 'fore:$(color.grey),back:$(color.white)'
property['style.bracelight'] = 'back:$(color.red),fore:$(color.black),bold'
property['style.bracebad'] = 'fore:$(color.red),bold'
property['style.controlchar'] = 'fore:$(color.grey)'
property['style.indentguide'] = 'fore:$(color.grey)'
property['style.calltip'] = 'fore:$(color.white),back:#444444'
property['style.folddisplaytext'] = 'fore:$(color.grey),back:$(color.white)'

fold.margin.colour = 'fore:$(color.grey),back:$(color.white)'

