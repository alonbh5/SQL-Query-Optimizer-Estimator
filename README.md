# SQL-Query-Optimizer-Estimator
Given a SQL query, Convert it To a Logical-query-plan, Optimize it, and Estimate The Size Of the Execution on the DB

R(A:INTEGER,B:INTEGER,C:INTEGER,D:INTEGER,E:INTEGER)
S(D:INTEGER,E:INTEGER,F:INTEGER,H:INTEGER,I:INTEGER)

Rules: 


- #4 Pushing Selections: πAσA=5∧B<D(R × S) -> πAσB<D(σA=5(R) × S)
- #4a Swaping Selections:  πAσB<D(σA=5(R) × S) - >  πAσA=5(σB<D(R) × S)
- #5  Swaping Selections and Projections where possible: πAσA=5(R × S) -> σA=5πA(R × S) 
- #6 Introduce Projections where possible(left): πAσA=5∧B<D(R × S)  ->  πA(σA=5(R) ×(JOIN B<D) B<DπD(S))
- #6a Introduce Projections where possible(right):
- 11b Recognizing joins: πAσB<D(σA=5(R) × S)  ->  πA(σA=5(R) ×(JOIN B<D) S)

Input - Valid SQL;

Output - Logical-query-plan

In The Menu Choose Between:

1. Apply Specific Rule
2. Run 10 Random Rules On 4 Different Cases
3. Size Estimation Of the Execution of the 4 Cases (will run (2) if user did not created before)
