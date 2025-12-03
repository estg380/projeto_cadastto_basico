import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- 1. FUNÇÃO DE CONFIGURAÇÃO DO BANCO DE DADOS ---
def configurar_banco():
    """Conecta ao SQLite e cria a tabela 'pessoas' se ela não existir."""
    try:
        # Tenta conectar ao banco de dados
        conexao = sqlite3.connect('cadastro.db')
        cursor = conexao.cursor()
        
        # Cria a tabela
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            nome TEXT NOT NULL,
            idade INTEGER,
            sexo TEXT
        );
        """)
        conexao.commit()
        return conexao
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Falha ao conectar ou criar tabela: {e}")
        return None

# --- 2. FUNÇÃO PARA INSERIR DADOS ---
def inserir_dados():
    """Coleta dados dos campos, valida e insere no banco de dados."""
    nome = entry_nome.get()
    idade_str = entry_idade.get()
    sexo = var_sexo.get()
    
    # Validação simples dos dados
    if not nome or not idade_str or not sexo:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
        return

    try:
        # Tenta converter idade para inteiro
        idade = int(idade_str)
        if idade <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro de Idade", "A idade deve ser um número inteiro positivo.")
        return

    # Conexão com o Banco de Dados (reutilizamos a conexão ou a criamos novamente)
    conexao = configurar_banco()
    if conexao is None:
        return
        
    cursor = conexao.cursor()
    dados = (nome, idade, sexo)
    
    # Inserção no banco de dados
    try:
        cursor.execute("INSERT INTO pessoas (nome, idade, sexo) VALUES (?, ?, ?)", dados)
        conexao.commit()
        messagebox.showinfo("Sucesso", f"Pessoa {nome} cadastrada com sucesso!")
        
        # Limpar os campos após o cadastro
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        var_sexo.set('') # Limpa a seleção do ComboBox
        
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Inserção", f"Não foi possível inserir os dados: {e}")
    finally:
        conexao.close()



# --- 3. CONFIGURAÇÃO DA INTERFACE GRÁFICA (TKINTER) ---

# Configuração da janela principal
janela = tk.Tk()
janela.title("Sistema de Cadastro")

# Frame principal para organizar os widgets com padding
frm = ttk.Frame(janela, padding="20")
frm.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#Widgets para nome
ttk.Label(frm,text="Nome:").grid(column=0, row=0, sticky=tk.W, pady=5)
entry_nome = ttk.Entry(frm,width=40)
entry_nome.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=10, pady=5)

#Widgets para idade
ttk.Label(frm,text="Idade:").grid(column=0 , row=1, sticky=tk.W, pady=5)
entry_idade = ttk.Entry(frm,width=10)
entry_idade.grid(column=1,row=1, sticky=tk.W, padx=10, pady=5)

#Widgats para sexo
ttk.Label(frm, text="Sexo:").grid(column=0, row=2, sticky=tk.W, pady=5)
var_sexo = tk.StringVar()
combo_sexo = ttk.Combobox(frm, textvariable=var_sexo, value=['Masculino','Feminino','Outro'], state='readonly', width=15)
combo_sexo.grid(column=1,row=2, sticky=tk.W, padx=10, pady=5)

#configurar botão de cadastro
btn_cadastrar = ttk.Button(frm, text="Cadastrar", command=inserir_dados)
btn_cadastrar.grid(column=1, row=3, sticky=tk.E , pady=20)

janela.mainloop()
