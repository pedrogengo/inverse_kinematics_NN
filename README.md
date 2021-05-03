# Cinemática Inversa de um manipulador de 3 Graus de Liberdade usando Redes Neurais

## Autores:
- Lucas Nicolau Aperguis
- Pedro Gabriel Gengo Lourenço

## Introdução:

Esse projeto foi desenvolvido como trabalho de graduação do curso de Engenharia de Instrumentação, Automação e Robótica da Universidade Federal do ABC. No presente trabalho, visamos construir um modelo que fosse capaz de realizar a cinemática inversa de um manipulador robótico, ou seja, que, dado um ponto cartesiano ((x,y,z)), seja capaz de retornar os ângulos ((θ_1, θ_2, θ_3)).

## Desenvolvimento:

Podemos dividir o desenvolvimento em x etapas:

- Criação do ambiente de simulação (Braço robótico e sua atualização);
- Geração da base de dados contendo os valores de ângulos e das coordenadas cartesianas;
- Treinamento e validação da rede neural;
- Análise dos resultados.