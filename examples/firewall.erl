%%  Author: Emanuele
%%  Created: 2012
%%  Description:
%%
%%     A firewall process protects another process (implementing a "partial function")
%%     from bad requests.
%%
%%     In order to verify that soter:error() is not called
%%     a Data_1 (`-D 1`) data abstraction is needed to refine the bindings of X
%%     in the `firewall` function.
%%

-module(firewall).
-compile(export_all).

-include_lib("soter.hrl").
-include_lib("grammars.hrl").

main() -> start(?list_of_peanos()).

start(S) ->
	Srv = spawn(fun() -> server(fun(X)->pred(X)end) end),
	Fir = spawn(fun() -> server(firewall(Srv,fun(X)-> notZero(X) end)) end),
	sendall(Fir, S),
	ok.

sendall(To, []) -> ok;
sendall(To, [X|Xs]) -> To ! {call, self(), X},
					   sendall(To, Xs).

%% property to be verified: unreachability of erlang:error()
pred(zero) -> ?soter_error("pred called with zero");
pred({s,N}) -> N.

notZero(zero) -> false;
notZero({s,_}) -> true.

server(HandleCall)->
	receive
		{call, From, Par} -> From ! {answer, self(), HandleCall(Par)}
	end,
	server(HandleCall).

firewall(Proc, Test) ->
	fun(X) ->
		case Test(X) of
			true  -> Proc ! {call, self(), X},
					 receive
					 	{answer, Proc, Res} -> Res
					 end;
			false -> bad_req
		end
	end.
