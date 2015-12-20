#!/usr/bin/python3
#-*- coding: utf-8 -*- 
#
#patrickernandes@gmail.com
#
"""Programa Controle"""
import os, sys
import time, datetime  #print (time.strftime("%H:%M:%S"))
import sqlite3
from tabulate import tabulate

#VARIAVEIS:
AUTOR = 'Patrick Ernandes'
VER = '0.1 '
MES = 'Abril/2015'
EMAIL = 'patrickernandes@gmail.com'
DB = 'CONTROLE.DB'


def menu():
    if os.path.isfile(DB) and os.access(DB, os.R_OK):        
        conecta = conectaBanco()
        file = 'true'
    else:
        print ('\nERROR: Arquivo de banco de dados ' + DB + ' não encontrado!')
        file = 'false'
    linha = input('\n[CONTROLE>] ').split(' ')
#    linha = linha.lower()
    if linha == '':
        help()
        main()
    elif linha[0] == 'hora':
        hora()
        menu()
    elif linha[0] == 'data':
        data()
        menu()
    elif linha[0] == 'help':
        help()
        main()
    elif linha[0] == 'quit':
        print ('Goodbye!')
        conecta.close()
        sys.exit()		
    elif linha[0] == 'exit':
        print ('Goodbye!')
        conecta.close()
        sys.exit()		
    elif linha[0] == 'versao':
        versao()
    elif linha[0] == 'criadb':
        criadb()
    elif linha[0] == 'cliente':
        if file == 'false':
            menu()
        else:
            cliente(conecta)
    elif linha[0] == 'ping':
        hora()
        if len(linha) > 1:
           ping(linha[1])
        menu()
    elif linha[0] == 'teste':
        versao()
        main()
    elif linha[0] == 'teste1':
        versao()
        main()
    else:
        hora()
        print ('\nComando não encontrado[]!')
        help()
        main()


def versao():
    print('''
                     _             _      
      ___ ___  _ __ | |_ _ __ ___ | | ___ 
     / __/ _ \| '_ \| __| '__/ _ \| |/ _ \    
    | (_| (_) | | | | |_| | | (_) | |  __/
     \___\___/|_| |_|\__|_|  \___/|_|\___|       

	''')
    print ("Versao: {}".format(VER + MES))
    print ("Autor : {}".format(AUTOR))
    print ("Email : {}".format(EMAIL))
    menu()
    
    
def criadb():     
    #conectando...
    conn = sqlite3.connect(DB)
    #definindo um cursor
    cursor = conn.cursor()

    #criando a tabela (schema)
    cursor.execute("""
    CREATE TABLE cliente (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        razao_social TEXT,
        cpf_cnpj TEXT,
        rua TEXT,
        numero TEXT,
        bairro TEXT,
        complemento TEXT,
        cidade TEXT,
        uf VARCHAR(2),
        cep TEXT,
        telefone TEXT,
        celular TEXT,
        email TEXT,
        contato TEXT,
        criado_em DATE NOT NULL
        );
    """)

    print('MSG: Arquivo de banco de dados ' + DB + ' criado!')
    #desconectando...
    conn.close()
    file = 'true'
    menu()

    
def conectaBanco():
    try:
        conn = sqlite3.connect(DB)        
        #print("conectado!")
    except Exception:
        print("ERRO: Sem acesso ao Banco!")
        print('Goodbye!')
        time.sleep(2)        
    return conn


def help():
    print ('''
    Use:
    -------
    versao    - informa a versao deste aplicativo
    help      - ajuda
    quit/exit - sai do programa
    criadb    - cria um novo arquivo de banco de dados
    cliente   - controle de clientes   
    ''')
    menu()
    
    
def cliente(conecta):
    linha = input('\n[CONTROLE>CLIENTE>] ').split(' ')
    #linha = linha.lower()
    if linha[0] == '':
        hora()
        cliente_help(conecta)        
    elif linha[0] == 'help':
        hora()
        cliente_help(conecta)
    elif linha[0] == 'quit':
        menu()
    elif linha[0] == 'exit':
        print ('Goodbye!')
        sys.exit()
    elif linha[0] == 'show':
        hora()
        cliente_show(conecta,linha);
    elif linha[0] == 'add':
        hora()
        cliente_add(conecta,linha)
    elif linha[0] == 'id':
        hora()
        cliente_id_validar(conecta,linha)
    elif linha[0] == 'del':
        hora()
        cliente_del(conecta,linha)
    else:
        cliente(conecta)
        

def cliente_help(conecta):
    print('''
    Use:
    -------
    show        - exibe os clientes
    show [nome] - exibe cliente pelo nome
    add [nome]  - adiciona um cliente 
    id [id]     - entra em modo cliente 
    del [id]    - exclui o cliente
    quit        - sai do modo controle de clientes
    exit        - sai do programa
    ''')
    cliente(conecta)


def cliente_show(conecta,linha):
    client = ' '.join(linha[1::])
    cur = conecta.cursor()
    
    if len(client) > 1:
        cur.execute("select id,nome,telefone,celular,contato from cliente where nome like ?", ('%'+client+'%',))
        row = cur.fetchone()
        if row is None:
            print('MSG: Cliente não encontrado!')
            cliente(conecta)
        else:
            header = ['ID', 'NOME', 'TELEFONE', 'CELULAR', 'CONTATO']
            m = []
            cur.execute("select id,nome,telefone,celular,contato from cliente where nome like ?",  ('%'+client+'%',))
            for row in cur:
                l = [row[0], row[1], row[2], row[3], row[4]]
                m.append(l)
                  
            print('\n')  
            print(tabulate(m, headers = header, tablefmt = 'orgtbl', numalign = 'right', stralign = 'left'))
            cliente(conecta)
    else:
        header = ['ID', 'NOME', 'TELEFONE', 'CELULAR', 'CONTATO']
        m = []
        #cur = conecta.cursor()
        cur.execute('select id, nome, telefone, celular, contato from cliente')
        for row in cur:
            l = [row[0], row[1], row[2], row[3], row[4]]
            m.append(l)
        
        print('\n')
        print(tabulate(m, headers = header, tablefmt = 'orgtbl', numalign = 'right', stralign = 'left'))        
        cliente(conecta)
    
    
def cliente_add(conecta,linha):
#    print(linha)
    data = time.strftime('%Y-%m-%d')
    client = ' '.join(linha[1::]).upper()
    cur = conecta.cursor()
        
    if len(client) > 1:
        cur.execute("select nome from cliente where nome=?", ([client]))
        row = cur.fetchone()
        if row is None:
            try:
                cur.execute('insert into cliente(nome, criado_em) VALUES(?, ?)', (client, data))
                conecta.commit()            
            except TypeError:
                print ('ERROR: Could not INSERT')
        
            cur.execute('select id from cliente where nome=?', ([client]))
            for row in cur:
                print('\nCliente novo, [ID>] ', (row[0]))
        
            cliente(conecta)
        else:
            print('ERROR: Cliente já cadastrado!')
            cliente(conecta)
    else:
        hora()
        cliente(conecta)

    
def cliente_id_help(conecta,id):
	print ('''
    Use:
    -------
    show                          - informações sobre cliente 
    set nome [nome]               - definir nome 
    set razao [razao]             - definir razao social
    set cpf [cpf]                 - definir cpf 
    set cnpj [cnpj]               - definir cnpj
    set rua [rua]                 - definir rua 
    set numero [numero]           - definir numero
    set bairro [bairro]           - definir bairro
    set complemento [complemento] - definir complemento
    set cidade [cidade]           - definir cidade
    set uf [uf]                   - definir uf
    set cep [cep]                 - definir CEP 
    set telefone [telefone]       - definir telefone
    set celular [celular]         - definir celular
    set email [e-mail]            - definir e-mail
    set contato [contato]         - definir contato
    quit                          - sai do cliente
    exit                          - sai do programa
    ''')
	cliente_id(conecta,id)    

    
def cliente_id_validar(conecta,linha):
#    print(linha)
    id = ' '.join(linha[1::])
    cur = conecta.cursor()
    if len(id) > 0:
        cur.execute('select id from cliente where id=?', ([id]))
        row = cur.fetchone()
        if row is None:
            print('ERROR: Cliente inexistente!')
            cliente(conecta)
        else:
            cliente_id(conecta,id)
    else:
        print('\nERROR: informar um ID')
        cliente(conecta)
    
        
def cliente_id(conecta,id):
#    print('\n[id>] ' +id)
    linha = input('\n[CONTROLE>CLIENTE>' + id + '>] ').split(' ')
    if linha[0] == '':
        hora()
        cliente_id_help(conecta,id)        
    elif linha[0] == 'help':
        hora()
        cliente_id_help(conecta,id)
    elif linha[0] == 'quit':
        cliente(conecta)
    elif linha[0] == 'exit':
        print ('Goodbye!')
        sys.exit()        
    elif linha[0] == 'show':
        hora()
        cliente_id_show(conecta,id)
    elif linha[0] == 'set':
        hora()
        cliente_id_set(conecta,id,linha)
    else:
        hora()
        cliente_id(conecta,id)
    

def cliente_id_show(conecta,id):
    cur = conecta.cursor()
    cur.execute("select nome,razao_social,cpf_cnpj,rua,numero,bairro,complemento,cidade,uf,cep, \
                 telefone,celular,email,contato,criado_em from cliente where id=?", ([id]))
    for row in cur:
        print('\n[NOME>]         %s' % row[0])
        print('[RAZAO SOCIAL>] %s' % row[1])
        print('[CPF/CNPJ>]     %s' % row[2])
        print('[RUA>]          %s' % row[3])
        print('[NUMERO>]       %s' % row[4])
        print('[BAIRRO>]       %s' % row[5])
        print('[COMPLEMENTO>]  %s' % row[6])
        print('[CIDADE>]       %s' % row[7])
        print('[UF>]           %s' % row[8])
        print('[CEP>]          %s' % row[9])
        print('[TELEFONE>]     %s' % row[10])
        print('[CELULAR>]      %s' % row[11])
        print('[E-MAIL>]       %s' % row[12])
        print('[CONTATO>]      %s' % row[13])
        print('[CRIADO_EM>]    %s' % row[14])
 
    cliente_id(conecta,id)
    

def cliente_id_set(conecta,id,linha):
    #print(linha)
    cur = conecta.cursor()
    
    if len(linha) > 1:          
        if linha[1] == 'nome':      
            nome = ' '.join(linha[2::]).upper()
            if nome == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set nome=? where id=?', (nome, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[NOME>] ' + nome)
                cliente_id(conecta,id)
            
        elif linha[1] == 'razao':
            razao = ' '.join(linha[2::]).upper()
            if razao == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set razao_social=? where id=?', (razao, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[RAZAO>] ' + razao)
                cliente_id(conecta,id)            
        
        elif linha[1] == 'cpf':
            cpf = ' '.join(linha[2::])          
            if cpf == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set cpf_cnpj=? where id=?', (cpf, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[CPF/CNPJ>] ' + cpf)
                cliente_id(conecta,id)
            
        elif linha[1] == 'cnpj':
            cnpj = ' '.join(linha[2::])
            if cnpj == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set cpf_cnpj=? where id=?', (cnpj, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[CPF/CNPJ>] ' + cnpj)
                cliente_id(conecta,id)
                
        elif linha[1] == 'rua':
            rua = ' '.join(linha[2::]).upper()
            if rua == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set rua=? where id=?', (rua, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[RUA>] ' + rua)
                cliente_id(conecta,id)
                
        elif linha[1] == 'numero':
            numero = ' '.join(linha[2::])
            if numero == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set numero=? where id=?', (numero, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[NUMERO>] ' + numero)
                cliente_id(conecta,id)
                
        elif linha[1] == 'bairro':
            bairro = ' '.join(linha[2::]).upper()
            if bairro == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set bairro=? where id=?', (bairro, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[BAIRRO>] ' + bairro)
                cliente_id(conecta,id)
                
        elif linha[1] == 'complemento':
            complemento = ' '.join(linha[2::]).upper()
            if complemento == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set complemento=? where id=?', (complemento, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[COMPLEMENTO>] ' + complemento)
                cliente_id(conecta,id)
                
        elif linha[1] == 'cidade':
            cidade = ' '.join(linha[2::]).upper()
            if cidade == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set cidade=? where id=?', (cidade, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[CIDADE>] ' + cidade)
                cliente_id(conecta,id)

        elif linha[1] == 'uf':
            uf = ' '.join(linha[2::]).upper()
            if uf == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set uf=? where id=?', (uf, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[UF>] ' + uf)
                cliente_id(conecta,id)
                
        elif linha[1] == 'cep':
            cep = ' '.join(linha[2::])
            if cep == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set cep=? where id=?', (cep, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[CEP>] ' + cep)
                cliente_id(conecta,id)
                
        elif linha[1] == 'telefone':
            telefone = ' '.join(linha[2::])
            if telefone == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set telefone=? where id=?', (telefone, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[TELEFONE>] ' + telefone)
                cliente_id(conecta,id)
                
        elif linha[1] == 'celular':
            celular = ' '.join(linha[2::])
            if celular == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set celular=? where id=?', (celular, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[CELULAR>] ' + celular)
                cliente_id(conecta,id)
                
        elif linha[1] == 'email':
            email = ' '.join(linha[2::])
            if email == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set email=? where id=?', (email, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[E-MAIL>] ' + email)
                cliente_id(conecta,id)
                
        elif linha[1] == 'contato':
            contato = ' '.join(linha[2::]).upper()
            if contato == '':
                cliente_id(conecta,id)
            else:
                try:
                    cur.execute('update cliente set contato=? where id=?', (contato, id)) 
                    conecta.commit()
                except TypeError:
                    print ('ERROR: update não realizado!')
                print('\n[CONTATO>] ' + contato)
                cliente_id(conecta,id)
                
        else:
            print('\nERROR!')
            cliente_id(conecta,id)
    else:
        cliente_id(conecta,id)


def cliente_del(conecta,linha):
    #print(linha)
    id = ' '.join(linha[1::])
    cur = conecta.cursor()
    if len(id) > 0:
        cur.execute('select id from cliente where id=?', ([id]))
        row = cur.fetchone()
        if row is None:
            print('ERROR: Cliente inexistente!')
            cliente(conecta)
        else:    
            try:
                cur.execute('delete from cliente where id=?', (id)) 
                conecta.commit()
            except TypeError:
                print ('ERROR: cliente não excluído!')
            print('\nCliente excluído, [ID>] ' + id)
            cliente(conecta)
    else:
        print('\nERROR: informar um ID')
        cliente(conecta)



#########MAIN##########
def main():
    print ('Inicio do programa:')
    print ('---\nCONTROLE:')
    print ('--------------------------------------------------------')   
    print ('Digite exit + [enter] para sair e help para ajuda.')
    menu()
    
def hora():
    print(time.strftime("[%H:%M:%S]"))
    
def data():
    print(time.strftime("%Y-%m-%d"))

def home():
    os.system('cd %USERPROFILE%')
    
    
    
###FIM#####
if __name__ == '__main__':
    main()
