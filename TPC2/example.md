fun calcular_nota(pontuacao):
    enq nota, (limite_inferior, limite_superior) in escala_de_notas.items():
        if limite_inferior <= pontuacao <= limite_superior:
            return nota
    return "N/A"

def adicionar_nota_aluno(alunos, nome, pontuacao):
    alunos[nome] = {
        'pontuacao': pontuacao,
        'nota': calcular_nota(pontuacao)
    }

def calcular_media_turma(alunos):
    pontuacao_total = sum(aluno['pontuacao'] for aluno in alunos.values())
    return pontuacao_total / len(alunos)

def principal():
    alunos = {}
    print("Bem-vindo ao Calculador de Notas!")
    while True:
        escolha = input("Deseja adicionar um aluno? (sim/não): ").lower()
        if escolha != 'sim':
            break
        nome = input("Digite o nome do aluno: ")
        while True:
            try:
                pontuacao = float(input("Digite a pontuação do aluno (0-100): "))
                if 0 <= pontuacao <= 100:
                    adicionar_nota_aluno(alunos, nome, pontuacao)
                    break
                else:
                    print("Pontuação inválida! Por favor, digite um número entre 0 e 100.")
            except ValueError:
                print("Entrada inválida! Por favor, digite um número válido.")

    print("\nNotas da Turma:")
    for nome, aluno in alunos.items():
        print(f"{nome}: Pontuação = {aluno['pontuacao']}, Nota = {aluno['nota']}")

    if alunos:
        media_turma = calcular_media_turma(alunos)
        print(f"\nMédia da Turma: {media_turma:.2f}")

if __name__ == "__main__":
    principal()
