# 1. Garante que todas as mudancas de arquivos deletados/adicionados entrem
git add -A

# 2. Garante que o .env NAO ESTA no commit por seguranca
git reset HEAD .env

# 3. Faz o commit usando o arquivo com a mensagem que criei antes
git commit -F .git/COMMIT_EDITMSG

# 4. Faz o push para o GitHub (certifique-se de estar na branch principal)
git push origin main
