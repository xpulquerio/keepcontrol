/*Resumo dos UPDATE*/
UPDATE public.accounts_userepisodeserie
	SET date_watched='01-04-2023'
	where date_watched between '08-07-2023 18:30' and '08-07-2023 23:59';
	
Select * from public.accounts_userepisodeserie 
where date_watched between '08-07-2023 18:30' and '08-07-2023 23:59';