// grammar for the language { a^n b^(2n) }
grammar Exo5;


// ===== LEXER RULES =====

A: 'a';
B: 'b';
WS: [ \t\r\nc-zC-Z]+ -> skip; // skip spaces, tabs, newlines


// ===== parser rules =====

r: expr EOF;

expr: A expr B B
    |
    ;