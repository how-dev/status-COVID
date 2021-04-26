# Status Covid

`Ideia:`

>A ideia é que você gere seu histórico da pandemia. Se já pegou Covid, se já foi vacinado, quantas doses, os testes que já fez e seus respectivos resultados.


## CLI commands:

>`flask database drop`: Apaga todas as tabelas.

>`flask database create`: Cria todas as tabelas.

>`flask user create {quantidade}` Cria `quantidade` usuários

>`flask vaccine create {quantidade} {min}-{max}` Cria `quantidade` vacinas para usuários de id `min` até `max` (inclusive) 

>`flask test create {quantidade} {min}-{max}` Cria `quantidade` testes de covid para usuários de id `min` até `max` (inclusive)
 
>`flask company create {quantidade}` Cria `quantidade` empresas no database.
 
> `flask admin create {quantidade}` Cria `quantidade` admins no database.

|        |  database drop         | database create  | user create {quantidade} | vaccine create {quantidade} {min}-{max}`| test create {quantidade} {min}-{max}|     company create {quantidade}|   admin create {quantidade}|
|--------|------------------------|------------------|--------------------------|-----------------------------------------|-------------------------------------|--------------------------------|----------------------------|
|  flask |  Deleta tabelas        | Cria tabelas     | Cria quantidade usuarios | Cria quantidade vacinas num range       | Cria quantidade testes num range    |     Cria quantidade empresas   |   Cria quantidade admin    |


## Rotas:

url_base = `futuramente...`

>`url_base/`users/:

=> `POST`:

        {
            "name": "{nome de usuário, string}",
            "age": {idade, integer},
            "email": "{string}",
            "document": "{CPF, string, máx=11}",
            "live_with": {vive com quantas pessoas, integer},
            "exposed_works": {Trabalha em contato com muitas pessoas? Boolean, não obrigatório},
            "password": {senha, string}
        }
    
Deve retornar: **201**

=> `GET`:
    
    {Sem conteúdo, retorna todos os usuários}

Deve retornar: **302**

>`url_base/`users/<user_id>:

=> `GET`:
    
    {Sem conteúdo, retorna um usuário com mesmo id do parâmetro}

Deve retornar: **200**

=> `PATCH, PUT`:

    {Propriedades que quer atualizar}

Deve retornar: **200**

=> `DELETE`:
    
    {Sem conteúdo, deleta o usuário passado por parâmetro}

Deve retornar: **204**

>`url_base/`users/login:

=> `POST`:

    {
        "email": ...
        "password": ...
    }

Deve retornar: 

**200**    

    {
        "user" : {
            "id": ...
            "name": ...
            "token": ...
        }
    }

>`url_base/`vaccine/:

=> `POST`:

    {
        "name": {nome da vacina, string},
        "record": {registro da vacina, string},
        "voucher": {url da foto do comprovante da vacina, strting},
        "user_id": {id de quem foi vacinado}
    }

Deve retornar: **201**

=> `GET`:
    
    {
        "vaccines": [
        {
           "id": ...,
           "name": ...,
           "record": ...,
           "voucher": ...
        },
        {
           "id": ...,
           "name": ...,
           "record": ...,
           "voucher": ...
        }, 
        ...Lista de vacinas...
        ]
    }

Deve retornar: **302**

>`url_base/`tests/:

=> `POST`:
    
    {
        "date_stamp": {data da vacina, string},
        "result": {resultado da vacina, boolean},
        "user_id": {id de em quem foi feito o teste, integer}
    }

Deve retornar: **201**

>`url_base/`tests/<user_id>:

=> `GET`:

    {
        "tests": [
            {
                "date_stamp": ...,
                "result": ...,
                "user": ...,
            },
            {
                "date_stamp": ...,
                "result": ...,
                "user": ...,
            },
            ...Lista de Testes de um usuário...
        ]
    }

Deve retornar: **302**

>`url_base/`tests/<test_id>:

=> `GET`:
    
    {
        "test": {
            "date_stamp": ...,
            "result": ...
        }
    }

Deve retornar: **302**
