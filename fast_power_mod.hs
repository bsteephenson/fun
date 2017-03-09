#!/usr/bin/env stack
-- stack --install-ghc runghc

import System.Environment

main = do

    args <- getArgs
    case length(args) of
        3 ->
            let (b:p:m:_) = args
            in print $ pow (read b) (read p) (read m)
        _ -> print "Correct usage is <base> <power> <mod> to find base^power in Z_mod"

binary 0 = [0]
binary 1 = [1]
binary x = (x `mod` 2) : (binary $ x `div` 2)

mult x y m = (x * y) `mod` m

-- b base, p power, m mod
pow b p m =
    let
        it [] _ = 1
        it (0:xs) b = it xs $ mult b b m
        it (1:xs) b = mult b (it xs $ mult b b m) m
    in it (binary p) b
