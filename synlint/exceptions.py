ParserException = type('ParserException', (Exception,), {})
ParserWarning = type('ParserWarning', (ParserException,), {})
ParserError = type('ParserError', (ParserException,), {})
