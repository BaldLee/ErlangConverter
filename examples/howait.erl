%% Author: Emanuele
%% Created: 06/mar/2012
%% Description:
%%
%%     This example defines a higher-order
%%     combinator that spawns a number of identical workers,
%%     each applied to a different task in a list.
%%     It then waits for all the workers to return a result
%%     before collecting them in a list which is subsequently returned.
%%     The desired property is that the combinator only returns
%%     when every worker has sent back its result.
%%
%%     Unfortunately to prove this property, stack reasoning is
%%     required, which is beyond the capabilities of an ACS.
%%
%%     This example has been designed to show some limitiations
%%     of Soter with respect to the control-flow abstraction:
%%     no finite state abstraction for the control-states can
%%     capture precisely the behaviour of the stack.
%%

-module(howait).
-compile(export_all).

-include_lib("soter.hrl").

-uncoverable("worker_finished >= 1, wait_over >= 1").

-include_lib("grammars.hrl").


serve()->
    receive
        {req, P, X} ->
            P ! {reply, self(), {s,X}},
            serve()
    end.


client(S,N)->
    S ! {req, self(), N},
    receive
        {reply, S, R} -> R
    end.

sp_wait(F, N) -> sp_wait(F, fun()->[] end, N).
sp_wait(_, G, zero) -> G();
sp_wait(F, G, {s,N}) ->
    S=self(),
    Clone = spawn(fun() ->
                    Res = F({s,N}),
                    ?label(worker_finished),
                    S ! {result, self(), Res }
                  end),
    sp_wait(F, fun() -> receive {result, Clone, R} -> [ R | G() ] end end, N).

main()->
    N = ?any_peano(),
    Server = spawn(fun() -> serve() end),
    sp_wait(fun(X)->client(Server, X) end, N),
    ?label(wait_over).

%%% Property:
%%% For each N any state where start returns and
%%% any of the spawned clients did not terminate
%%% is NOT reachable
