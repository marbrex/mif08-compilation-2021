// define a tiny grammar for Well-founded parenthesis 
grammar Exo4;


// ===== LEXER RULES =====

CHARS: ~[()[\]] -> skip; // skip everything except paranthesises


// ===== parser rules =====

r: prths EOF;

prths: '(' prths ')' prths
    |
    | '[' prths ']' prths
    ;
