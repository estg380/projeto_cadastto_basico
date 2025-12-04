import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry


# --- 1. FUNÇÃO DE CONFIGURAÇÃO DO BANCO DE DADOS ---
def configurar_banco():
    """Conecta ao SQLite e cria a tabela 'pessoas' se ela não existir."""
    try:
        conexao = sqlite3.connect('cadastro.db')
        cursor = conexao.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            nome TEXT NOT NULL,
            idade INTEGER,
            sexo TEXT,
            nascimento DATE
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
    
    # Validação simples
    if not nome or not idade_str or not sexo:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
        return

    try:
        idade = int(idade_str)
        if idade <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro de Idade", "A idade deve ser um número inteiro positivo.")
        return

    conexao = configurar_banco()
    if conexao is None:
        return
        
    cursor = conexao.cursor()
    dados = (nome, idade, sexo)
    
    try:
        cursor.execute("INSERT INTO pessoas (nome, idade, sexo, nascimento) VALUES (?, ?, ?)", dados)
        conexao.commit()
        messagebox.showinfo("Sucesso", f"Pessoa {nome} cadastrada com sucesso!")
        
        # Limpar campos e RECARREGAR o Treeview
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        var_sexo.set('')
        
        # Chama a função para atualizar a visualização
        carregar_dados_treeview() 
        
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Inserção", f"Não foi possível inserir os dados: {e}")
    finally:
        conexao.close()


# --- 3. FUNÇÃO PARA CARREGAR DADOS NO TREEVIEW ---
def carregar_dados_treeview():
    """Busca todos os dados no BD e insere no widget Treeview."""
    # 1. Limpa os dados existentes no Treeview
    for item in tree.get_children():
        tree.delete(item)

    # 2. Conecta ao Banco de Dados e busca os dados
    conexao = configurar_banco()
    if conexao is None:
        return
        
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT nome, idade, sexo, nascimento FROM pessoas ORDER BY nome ASC")
        dados = cursor.fetchall()
        
        # 3. Insere os novos dados no Treeview
        for registro in dados:
            tree.insert('', tk.END, values=registro)
            
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Leitura", f"Não foi possível carregar os dados: {e}")
    finally:
        conexao.close()

# --- 4. CONFIGURAÇÃO DA INTERFACE GRÁFICA (TKINTER) ---

# Configuração da janela principal
janela = tk.Tk()
janela.title("Sistema de Cadastro e Visualização")

# --- FRAME DE CADASTRO ---
frm_cadastro = ttk.LabelFrame(janela, text="Cadastro de Pessoas", padding="20")
# *** CORREÇÃO: Usando grid() para o frame de cadastro na janela ***
frm_cadastro.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Widgets para Nome
ttk.Label(frm_cadastro, text="Nome:").grid(column=0, row=0, sticky=tk.W, pady=5)
entry_nome = ttk.Entry(frm_cadastro, width=40)
entry_nome.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=10, pady=5)

# Widgets para Idade
ttk.Label(frm_cadastro, text="Idade:").grid(column=0, row=1, sticky=tk.W, pady=5)
entry_idade = ttk.Entry(frm_cadastro, width=10)
entry_idade.grid(column=1, row=1, sticky=tk.W, padx=10, pady=5)

# Widgets para Sexo
ttk.Label(frm_cadastro, text="Sexo:").grid(column=0, row=2, sticky=tk.W, pady=5)
var_sexo = tk.StringVar()
combo_sexo = ttk.Combobox(frm_cadastro, textvariable=var_sexo, values=['Masculino', 'Feminino', 'Outro'], state='readonly', width=15)
combo_sexo.grid(column=1, row=2, sticky=tk.W, padx=10, pady=5)

""" Widgets para data
ttk.Label(frm_cadastro, text="data").grid(column=0, row=3, sticky=tk.W, pady=5)
entry_idade = ttk.Entry(frm_cadastro, width=10)
entry_idade.grid(column=1, row=3, sticky=tk.W, padx=10, pady=5)"""

#Widgets para data de nascimento
ttk.Label(frm_cadastro, text="Nascimento").grid(column=0, row=3, sticky=tk.W, pady=5)
#Criando Widget dara entry
entry_nascimento = DateEntry(frm_cadastro, width=12, background='darkblue',
                             foreground='white', borderwidth=2, year=2000, date_pattern='dd/mm/yyyy' )
entry_nascimento.grid(column=1, row=3, sticky=tk.E, padx=10, pady=5)


# Botão de Cadastro
btn_cadastrar = ttk.Button(frm_cadastro, text="Cadastrar", command=inserir_dados)
btn_cadastrar.grid(column=1, row=3, sticky=tk.E, pady=10)

# Garante que o frame de cadastro se expanda na coluna 1
frm_cadastro.grid_columnconfigure(1, weight=1)

# --- FRAME DE VISUALIZAÇÃO ---
frm_visualizacao = ttk.LabelFrame(janela, text="Dados Cadastrados", padding="10")
# *** CORREÇÃO: Usando grid() para o frame de visualização na janela ***
frm_visualizacao.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configuração do Treeview (Tabela)
colunas = ("Nome", "Idade", "Sexo", "data")
tree = ttk.Treeview(frm_visualizacao, columns=colunas, show='headings')

# Define os cabeçalhos das colunas
for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=150)

# Adiciona uma barra de rolagem vertical
scrollbar = ttk.Scrollbar(frm_visualizacao, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Posiciona o Treeview e a Scrollbar DENTRO do frm_visualizacao (usando GRID)
tree.grid(row=0, column=0, sticky='nsew')
scrollbar.grid(row=0, column=1, sticky='ns')

# Configura o redimensionamento do frame de visualização para a Treeview
frm_visualizacao.grid_rowconfigure(0, weight=1)
frm_visualizacao.grid_columnconfigure(0, weight=1)

# *** Configuração de Redimensionamento da Janela Principal ***
janela.grid_columnconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1) # A linha 1 (onde está frm_visualizacao) se expande

# Carrega os dados na primeira execução
carregar_dados_treeview()

# Loop principal do Tkinter
janela.mainloop()
