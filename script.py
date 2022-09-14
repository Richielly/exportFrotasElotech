import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

nomeBanco = cfg['DEFAULT']['NomeBanco']
codEntidade = cfg['DEFAULT']['CodEntidade']
nomeEntidade = cfg['DEFAULT']['NomeEntidade']
motorista = cfg['DEFAULT']['Motorista']

scripts = {
'Entidade' : f""" select distinct cor ||'|' from siscop.pat_veiculo """,

'Cor' : f""" select distinct cor ||'|' from siscop.pat_veiculo """,

'Marca' : f""" select substring(descricao from 1 for 30) ||'|' as extractMarca
from siscop.fr_marcaveiculo """,

'Modelo' : f""" select
distinct
coalesce(substring(v.descricao from 1 for 60),'CONVERSÃO') ||'|'||
trim(coalesce(substring(mr.descricao from 1 for 30),'CONVERSÃO')) ||'|'||
coalesce(substring(e.descricao from 1 for 60),'CONVERSÃO') ||'|'||
coalesce(cast(p.codtribunal as varchar),'') ||'|' as extractModelo
from siscop.fr_modeloveiculo m
right join siscop.pat_veiculo v on (v.modeloveiculo = m.modeloveiculo)
left join siscop.fr_marcaveiculo mr on (mr.marca = m.marca)
left join siscop.fr_especieveiculos e on (e.codigo = v.especie)
left join siscop.pat_tipocombustivel p on (p.tipocombustivel = v.tipocombustivel) """,

'Especie' : f""" select
substring(e.descricao from 1 for 60) ||'|'||
'' ||'|'||
case e.tipomedicao
when 'V' then 1
when 'H' then 2
else '0' end ||'|'||
coalesce(cast(e.codtribunal as varchar),'') ||'|'||
'' ||'|' as extractEspecie
from siscop.fr_especieveiculos e """,

'Motorista' : f""" select
{codEntidade} ||'|'||
m.codigo ||'|'||
m.matriculafolha ||'|'||
'' ||'|'||
coalesce(m.cpf,'') ||'|'||
m.numerocnh ||'|'||
'1' ||'|'|| --com foto
coalesce(EXTRACT(day FROM m.dataprimhab) ||'/'|| EXTRACT(month FROM m.dataprimhab) ||'/'|| EXTRACT(year FROM m.dataprimhab),'01/01/1899') ||'|'||
coalesce(EXTRACT(day FROM m.validadecnh) ||'/'|| EXTRACT(month FROM m.validadecnh) ||'/'|| EXTRACT(year FROM m.validadecnh),'01/01/1899') ||'|'||
coalesce(EXTRACT(day FROM m.dataexpedicao) ||'/'|| EXTRACT(month FROM m.dataexpedicao) ||'/'|| EXTRACT(year FROM m.dataexpedicao),'01/01/1899') ||'|' as ExtractMotorista
from siscop.fr_motoristas m """,

'MotoristaCategoriaCnh' : f""" select
{codEntidade} ||'|'||
m.codigo ||'|'||
m.categcnh ||'|' as extractCategoriaCnh
from siscop.fr_motoristas m """,

'MotoristaSituacaoCnh' : f""" select
{codEntidade} ||'|'||
m.codigo ||'|'||
EXTRACT(day FROM current_date) ||'/'|| EXTRACT(month FROM current_date) ||'/'|| EXTRACT(year FROM current_date) ||'|'||
'1' ||'|'|| -- 1 - Normal / 2 - Suspenso
'0' ||'|' 
from siscop.fr_motoristas m """,

'Veiculo' : f""" select
distinct
{codEntidade} ||'|'||
v.bem ||'|'||
pb.chapa ||'|'||
coalesce(v.letraplaca || v.numeroplaca, '') ||'|'||
coalesce(substring(e.descricao from 1 for 60),'CONVERSÃO') ||'|'||
coalesce(substring(v.descricao from 1 for 60),'CONVERSÃO') ||'|'|| --Modelo
coalesce(v.cor,'CONVERSÃO') ||'|'||
coalesce(cast(v.renavan as varchar), '') ||'|'||
coalesce(cast(v.chassi as varchar), '') ||'|'||
'' ||'|'||
coalesce(cast(v.anofabr as varchar), '') ||'|'||
coalesce(cast(v.anomod as varchar), '') ||'|'||
coalesce(cast(v.capacidade as varchar), '1') ||'|'||
v.descricao ||'|'|| --DsObservacao
case v.medidorquebradosn
when 'N' then '1'
when 'S' then '2'
else '2' end ||'|'|| -- 1-Sim / 2-Não
'' ||'|'||
coalesce(cast(tc.codtribunal as varchar),'') ||'|'||
coalesce(EXTRACT(day FROM v.data_portal) ||'/'|| EXTRACT(month FROM v.data_portal) ||'/'|| EXTRACT(year FROM v.data_portal),'31/12/1899') ||'|'||
'0' ||'|'||
translate(upper(coalesce(cast(v.potencia as varchar),'0')),'CV','') ||'|'||
translate(coalesce(cast(v.qtdetanque as varchar),'0'),'.',',') ||'|'||
'0' ||'|'||
'1' ||'|'|| --ImpressaoDiarioBordo 1 - Sim
translate(coalesce(cast(v.mediacombustivel as varchar),''),'.',',') ||'|' as extractVeiculos
from siscop.pat_veiculo v
left join siscop.pat_bem pb on (pb.bem = v.bem)
left join siscop.fr_especieveiculos e on (e.codigo = v.especie)
left join siscop.fr_modeloveiculo m on (m.modeloveiculo = v.modeloveiculo)
left join siscop.pat_tipocombustivel tc on (tc.tipocombustivel = v.tipocombustivel)
where pb.tipo = 'V' """,

'Produto' : f""" select
distinct
coalesce(p.descricao,'') ||'|'||
coalesce(p.item,'') ||'|'||
'1' ||'|'|| -- 1 = combustivel 2 = Óleo/Lubrificante 3 = Peças 4 = Serviços 5 = Pneus 6 = Acessórios
'' ||'|'||
'' ||'|'||
'1' ||'|' as etractProduto -- 1 = Ativo 0 = Inativo
from siscop.pat_tipocombustivel p """,

'VeiculoProduto' : f""" select
distinct
{codEntidade} ||'|'||
v.bem ||'|'||
coalesce(p.item,'') ||'|'||
coalesce(p.descricao,'') ||'|' as extractVeiculoProduto
from siscop.pat_veiculo v
left join siscop.pat_tipocombustivel p on (p.tipocombustivel = v.tipocombustivel) """,

'Abastecimento' : f""" select 
{codEntidade} ||'|'||
coalesce(cast(a.numero as varchar),'') || coalesce(cast(a.exercicio as varchar),'') ||'|'|| 
coalesce(cast(v.bem as varchar),'') ||'|'||
coalesce(v.chapa,'') ||'|'||
coalesce(p.item,'6') ||'|'||
coalesce(p.descricao,'') ||'|'||
{motorista} ||'|'|| -- motorista = 1 matricula = 800	 cnh = 04749117173 padrão estabelecido pelas pessoas da entidade de Manoel Ribas
coalesce(translate(cast(i.valor as varchar),'.',','),'0,00') ||'|'||
EXTRACT(day FROM a.data) ||'/'|| EXTRACT(month FROM a.data) ||'/'|| EXTRACT(year FROM a.data) || ' ' || EXTRACT(HOUR FROM a.data) ||':'|| EXTRACT(MINUTE FROM a.data) ||':'|| EXTRACT(SECOND FROM a.data) ||'|'||
coalesce(translate(cast(i.quantidade as varchar),'.',','),'0') ||'|'||
coalesce(translate(cast(i.valortotal as varchar),'.',','),'0,00') ||'|'||
1 ||'|'||  -- 1 = Completo - 2 = Parcial
coalesce(cast(a.nota as varchar),'') ||'|'||
'Conversão, motorista incluído como padrão' ||'|'||
coalesce(cast(a.fornecedor as varchar),'') ||'|'||
coalesce(cast(f.cnpj as varchar),'') ||'|'||
'' ||'|'||
coalesce(case a.centrocusto 
	 when '1' then '2001' 
	 when '6' then '7002'
	 when '8' then '9001'
	 when '4' then '5002'
	 when '5' then '6002'
	 when '14' then '15001'
	 when '11' then '12002'
	 when '9' then '10002'
	 when '17' then '3003'
	 when '10' then '11002'
	 when '3' then '4003'
	 when '2' then '3004' end, '') ||'|'||
'' ||'|'||
1  ||'|'||
{codEntidade} ||'|'||
coalesce(cast(a.anoliquidacao as varchar), '') ||'|'||
coalesce(case a.anoliquidacao 
    when 2022 then '#liquidacao#' else cast(a.anoliquidacao as varchar) end, '') ||'|'||
--coalesce(cast(a.liquidacao as varchar), '') ||'|'||
coalesce(cast(a.anoliquidacao as varchar), '') ||'|'||
{codEntidade} ||'|'||
{codEntidade} ||'|'||
coalesce(cast(a.anoempenho as varchar), '') ||'|'||
coalesce(case a.anoempenho 
    when 2022 then '#empenho#' else cast(a.anoempenho as varchar) end, '') ||'|'||
--coalesce(cast(a.empenho as varchar), '') ||'|'||
coalesce(cast(a.anoempenho as varchar), '') ||'|'||
{codEntidade} ||'|' as extarctAbastecimento
from siscop.fr_gastosfrota a
left join siscop.fr_gastosfrotadespesas i on (i.exercicio = a.exercicio and i.numero = a.numero)
left join siscop.pat_veiculo v on (v.bem = a.veiculo)
left join siscop.pat_bem pb on (pb.bem = v.bem)
left join siscop.pat_tipocombustivel p on (p.tipocombustivel = v.tipocombustivel)
left join siscop.fornecedor f on (f.fornecedor = a.fornecedor)
where pb.tipo = 'V'
order by a.exercicio , a.numero, a.data 
 """,

'Acumulador' : f""" select
{codEntidade} ||'|'||
coalesce(cast(v.bem as varchar),'') ||'|'||
coalesce(v.chapa,'') ||'|'||
EXTRACT(day FROM a.data) ||'/'|| EXTRACT(month FROM a.data) ||'/'|| EXTRACT(year FROM a.data) || ' ' || EXTRACT(HOUR FROM a.data) ||':'|| EXTRACT(MINUTE FROM a.data) ||':'|| '#sec#' ||'|'||
'2' ||'|'|| --Abastecimento
coalesce(cast(a.numero as varchar),'') || coalesce(cast(a.exercicio as varchar),'') ||'|'||
coalesce(replace(cast(a.medicaoatual as varchar), '.',','),'0') ||'|'||
'' ||'|' as extractVeciculoAcumulador
from siscop.fr_gastosfrota a
left join siscop.pat_veiculo v on (v.bem = a.veiculo)
left join siscop.pat_bem pb on (pb.bem = v.bem)
where pb.tipo = 'V'
order by a.exercicio , a.numero, a."data" """
}