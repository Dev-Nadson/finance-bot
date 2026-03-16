import matplotlib.pyplot as plt
import io

x = [2, 4, 3, 8, 9]
y = [3, 5, 7, 3, 11]

def generate_chart_buffer():
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, linestyle='--', marker='o', color='red')
    plt.xlabel('Preço')
    plt.ylabel('Quantidade')
    plt.title('Gráfico de Finanças')
    plt.grid(True)

    # 2. Salva o gráfico em um buffer (memória RAM)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0) # Volta o "ponteiro" do arquivo para o início
    
    # 3. Limpa o Matplotlib para não acumular memória ou sobrepor gráficos
   # Exibe o gráfico (opcional, pode ser removido se não for necessário)
    plt.close()
    
    return buf