--[[
    Módulo para fazer as requisições HTTP no servidor Flask e usar o 
    banco de dados MySQL
    ]]


local HttpService = game:GetService("HttpService")
local url_base = "url_do_servidor"
local auth = "senha_para_autenticacao"

local module = {}

function module:GetAsync(key)
	return HttpService:JSONDecode(HttpService:RequestAsync({
		Url = url_base.."/user/"..key,
		Method = "GET",
		Headers = {
			["Content-Type"] = "application/json",
			["Authorization"] = auth
		}
	}).Body)
end

function module:SetAsync(key,value)
	HttpService:RequestAsync({
		Url = url_base.."/user/"..key,
		Method = "POST",
		Headers = {
			["Content-Type"] = "application/json",
			["Authorization"] = auth
		},
		Body = HttpService:JSONEncode(value)
	})
end

return module
