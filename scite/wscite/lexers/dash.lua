-- Copyright 2006-2017 Mitchell mitchell.att.foicica.com. See LICENSE.
-- Diff LPeg lexer.

local l = require('lexer')
local token, word_match = l.token, l.word_match
local P, R, S = lpeg.P, lpeg.R, lpeg.S

local M = {_NAME = 'dash'}

-- DIFF compatible line start
local exclamation = token('exclamation', P('!') * l.any^0)
local plus = token('plus', P('+') * l.any^0)
local minus = token('minus', P('-') * l.any^0)
local gt = token('gt', P('>') * l.any^0)
local lt = token('lt', P('<') * l.any^0)
local at2 = token('at2', P('@@') * l.any^0)
local at = token('at', P('@') * l.any^0)
local star = token('star', P('*') * l.any^0)
-- DIFF incompatible line start
local pipe = token('pipe', P('|') * l.any^0)
local hash = token('hash', P('#') * l.any^0)
local eq = token('eq', P('=') * l.any^0)
local tilde = token('tilde', P('~') * l.any^0)
local dolar = token('dolar', P('$') * l.any^0)
local percent = token('percent', P('%') * l.any^0)

M._rules = {
  {'exclamation', exclamation},
  {'plus', plus},
  {'minus', minus},
  {'gt', gt},
  {'lt', lt},
  {'at2', at2},
  {'at', at},
  {'star', star},
  {'pipe', pipe},
  {'hash', hash},
  {'eq', eq},
  {'tilde', tilde},
  {'dolar', dolar},
  {'percent', percent},
  
  {'any_line', token('default', l.any^1)},
}

M._tokenstyles = {
  star = 'fore:$(color.red),back:$(color.light),bold',
  exclamation = 'fore:$(color.grey)',
  plus = 'fore:$(color.blue),bold',
  minus = 'fore:$(color.red),bold',
  gt = 'fore:$(color.green),bold',
  at2 = 'fore:$(color.teal)',
  at = 'fore:$(color.purple)',
  lt = 'fore:$(color.orange),bold',

  eq = 'fore:$(color.yellow),bold',
  pipe = 'fore:$(color.yellow),bold',
  hash = 'fore:$(color.yellow),bold',
  tilde = 'fore:$(color.yellow),bold',
  dolar = 'fore:$(color.yellow),bold',
  percent = 'fore:$(color.yellow),bold',
}

M._LEXBYLINE = true

M._foldsymbols = {
  _patterns = {'%*'}
}

return M
