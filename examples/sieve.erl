%%  Author: Emanuele
%%  Created: 26/jul/2012
%%  Description:
%%
%%     Eratosthenes's Sieve, concurrent flavour.
%%     A counter acts as a generator of integers.
%%     These integers get forwarded or blocked by layers of filter processes
%%     each blocking the multiples of an (already produced) prime number.
%%     When a new prime number is produced a new filter for it is created.
%%     The main just prints all the messages that make it through the layers of filters.
%%
%%     Soter can prove that all the mailboxes of the filter processes always
%%     have at most 1 message queued.
%%
%%     Reference: Rob Pike, [Concurrency/message passing in Newsqueak](http://video.google.com/videoplay?docid=810232012617965344)
%%



-module (sieve).
-compile(export_all).

-include_lib("soter.hrl").
-include_lib("grammars.hrl").

-soter_config(peano).

-uncoverable("counter_mail >= 2").
-uncoverable("filter_mail >= 2").
-uncoverable("sieve_mail >= 2").

main() ->
    Me = self(),
    Gen = spawn(fun()->counter(2)end),
    spawn(fun()->sieve(Gen,Me)end),
    dump().

dump() ->
    receive
        X ->
            io:fwrite("~w~n", [X]),
            dump()
    end.

counter(N) ->
    ?label_mail("counter_mail"),
    receive
        {poke, From} ->
            From ! {ans, N},
            counter(N+1)
    end.

sieve(In, Out) ->
    ?label_mail("sieve_mail"),
    In ! {poke, self()},
    receive
        {ans,X} ->
            Out ! X,
            F = spawn(fun()->filter(divisible_by(X),In)end),
            sieve(F,Out)
    end.

% When poked, answers with a number that passes the Test,
% filtering the ones generated by In
filter(Test, In) ->
    ?label_mail("filter_mail"),
    receive
        {poke, From} ->
            filter(Test, In, From)
    end.

filter(Test, In, Out) ->
    In ! {poke, self()}, % Ironically, duplicating this line makes the program faster but the mailboxes become unbounded!
    receive
        {ans,Y} ->
            case Test(Y) of
                false -> Out ! {ans, Y}, filter(Test, In);
                true  -> filter(Test, In, Out)
            end
    end.

% Arithmetic operators are not supported by Soter
% A simple workaround is manually providing an abstraction
% for them.

% Here the macro SOTER allows us to use the normal definition
% when running the program through the interpreter and
% to use the mock one instead when analysing it with Soter.

-ifdef(SOTER).

    divisible_by(X) ->
        fun(Y) -> ?any_bool() end.

-else.

    divisible_by(X) ->
        fun(Y) ->
            case Y rem X of
                0 -> true;
                _ -> false
            end
        end.

-endif.
