# Retour d'Expérience (RETEX)

## 1. État d'esprit initial : Le flou total
Au début du projet, j'étais clairement perdu.
Je ne voyais pas par où commencer, ni comment tester quelque chose que je ne comprenais pas vraiment.
Le sujet semblait demander beaucoup de choses à la fois (serveur, algo, binaire, tests)
et je ne savais pas comment aborder le sujet, sans parler du prof qui ne pouvait pas nous répondre.
C'était un peu comme avancer à taton dans le noir pour essayer de trouver l'interrupteur de la lumière, ça m'a pris
du temps à comprendre le sens du sujet car j'ai souvent été tenté de faire un projet complet et ai eu du mal à ne faire
que des tests "dans le vide" sans vrai interface ni projet concret.

## 2. La stratégie : Simplifier pour comprendre
Plutôt que de foncer tête la première, j'ai décidé de tout remettre à plat pour rendre le projet plus "scolaire" et abordable :
J'ai créé un plan cohérent mais basé sur une tonne de tests car le but est de faire le plus de tests possible bien que je me
sois souvent questionné sur l'utilité de plusieurs d'entre-eux.
Après avoir réalisé le plan, j'ai opté pour un algorithme de triangulation simple (en éventail) car le but était le test, pas la performance pure, en tout cas c'est ce que je pense toujours.

## 3. L'apport de l'IA
Je ne m'en cache pas, j'ai utilisé l'IA pour m'aider à débloquer la situation et avancer plus vite :
    -   **Pour la Compréhension** : Je lui ai demandé de m'expliquer les formats binaires (Little Endian) et comment structurer les paquets de données, car c'était obscur pour moi au départ.
    -   **Génération de tests** : Une fois la logique comprise, j'ai utilisé l'IA pour générer des idées de tests unitaires (des cas limites et erreurs de parsing). Ça m'a permis de m'appuyer sur des tests cohérent pour mieux comprendre la structure et la logique attendues, ou en tout cas, globalement utilisée.
    -   **Les Mocks** : Pour les mocks, bien que je n'étais pas très à l'aise avec `unittest.mock`. Je n'ai pas utilisé l'IA bien que j'y étais tenté, les mocks n'étaient pas si dur à comprendre et à mettre en place, les documentations en ligne m'ont suffit.

## 4. Les commits et rendus
Lors des premières séances j'ai assez vite rendu un plan avec un stock de tests à réaliser.
Les délais ont facilement été tenus, mais arrivés aux dernières séances, je me suis vite perdu car j'avais une
vingtaine de tests et je voyais mes collègues en avoir 50/60, donc je me demande encore comme c'est possible d'en avoir
autant, car bien que j'ai compris l'utilité de mes tests, je dois en avoir 30 au maximum, actuellement.
Mes derniers commits ont été assez en décalé par rapport aux premiers mais je pense avoir fait le nécessaire pour ce projet.

## 5. Bilan
Finalement, ce projet m'a appris qu'on peut tester efficacement même un code complexe si on prend le temps de le simplifier et de l'isoler. L'IA a été un outil efficace pour combler mes lacunes techniques sur le moment, me permettant de me concentrer sur la logique des tests et la couverture des cas d'erreurs plutôt que de bloquer sur la syntaxe Python.
J'ai aussi et surtout avancé grâce au projet GLA que je réalise en parallèle en ILSEN, vu qu'il faut mettre en place des tests
j'ai compris la mise en situation et l'utilisation avec les fichiers .yaml et kubernetes.
Je suis assez satisfait de mon avancée, mais n'ai pour autant pas vraiment aimé la structure du cours "libre".
