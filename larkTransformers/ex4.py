ExprRelacional : Exp | Exp OPR Exp

    OPR : EQ | NE | LT | LE | GT | GE

    Exp : Termo | Exp OPA Termo

    Termo : Fator | Termo OPM Fator

    OPA : ADD | SUB | OR
    OPM : MUL | DIV | AND
    Fator : CINT | CREAL | CCHAR | CBOOL | LP ExprRelacional RP | InvocFuncao | OPU Fator

    GA = < GIC, A(X), RC(A), CC(p), RT(p) >
    GIC : 
    Lista : "(" Elems ")"
    Elems : Elem | Elems "," Elem
    Elem : NUM | PAL