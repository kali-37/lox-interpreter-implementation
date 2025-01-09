/*
Essentials of Parsing 
*/ 

/** 
    E 
       : T E'
       ;
**/
function E(){
    return T() && _E();
}




/** 
    E'
       : + T E'
       : eplision 
       ;
**/

function _E(){
    // + T E' 
    if (lookahead()=='+'){
    return term('+') && T() && _E();
    }
// eplision 
    return true;
}

// ----------------

/** 
 
 T 
   : F T' 
   ; 
**/

function T(){
    return (F() && _T());
}

/** 
 
 T' 
    : * F T'
    | eplision 
    ;
**/
  
function _T(){
    // * F T'
    if (lookahead()=='*'){
        return term('*') && F() && _T();
    }
    // eplision 
    return true;
}

//---------------------------------

/* 
  F 
     : NUMBER 
     ; 
*/
function F() {
    return term('a')
}

// ___________________________________

let source; 
let cursor  = 0 ;

function lookahead(){
    return source[cursor];
}

function term(expected){
    return source[cursor++] === expected;
}

/**
 
 Inatialize the parsing string and cursor.
 Attempts to parse a string starting from the main symbol
**/

function parse(s){
    source = s;
    cursor = 0;
    return E() && cursor === s.length;
}

import equal from 'assert'

equal(parse('a-'),true)
equal(parse('a+a'),true)
equal(parse('a'),true)
equal(parse('a*a*a*a*a*a'),true)

console.log("[PASS]")