[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/TF_T6rNL)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11286708&assignment_repo_type=AssignmentRepo)

Auteur : DO Frédéric & TRUONG Guillaume
Objectif : Créer le jeu Pac-man à la 1ère personne

TO DO :
    - créer la caméra à la première personne qui suit le joueur (fait)
    - créer la structure du labyrinthe (fait)
    - créer une fonction mouvement pour le joueur et les ennemies (fait)
    - implémenter les collisions entre les murs et le joueur (fait)
    - ajouter les points (fait)
    - ajouter une menu
    - implémenter une minimap pour se repérer (annulé)
    - ajouter des pommes (fait)
    - se téléporter entre les sorties du labyrinthe (fait)
    - ajouter de la musique (moitié fait)
    - créer des ennemies qui se déplacent dans le labyrinthe (fait)
    - ajouter le score (fait)
    - ajouter un écran de victoire et de défaite (fait)
    - ajouter un système d'invincibilité après avoir manger une pomme
    - ajouter les vies (fait)
    - créer une vue du dessus pour avoir une meilleure vue (fait)

Règles du jeu :
    - Il s'agit d'un Pac-man en 3D à la première personne, le but est comme dans le jeu original, c'est-à-dire de ramasser toute les points (boules blanches) dans le labyrinthe
    - Les mouvements se feront avec les touches ZQSD ainsi que des mouvements de caméra grâce à la souris
    - Si vous prennez une des 2 sorties du labyrinthe, vous serez téléporté à l'autre sortie comme dans le jeu originel
    - Lorsque vous marchez sur une boule blanche, elle disparaît et vous augmentez votre score qui est affiché avec l'appellation "score"
    - L'affichage "Points restants" vous indique le nombre de boules blanches restantes dans le labyrithe avant de gagner la partie.
    - Appuyer sur la touche "SPACE" vous fera voir la carte avec une vue du dessus du labyrinthe pour avoir une meilleure vision mais dans cet état, vous ne pourrez plus bouger
    - Appuyer sur la touche "LEFT_CONTROL" vous fera repasser en vue première personne, il est possible de se déplacer uniquement dans cette état
    - 4 ennemies se déplacent aléatoirement dans le labyrinthe. Ils changent de direction toutes les 7 secondes ou lorsqu'ils touchent un mur.
    - Toucher un ennemi fait perdre une vie (3 vie au départ) et téléporte le joueur au centre du labyrinthe. Si le joueur n'a plus de vie il perd la partie. 

Pour aller plus loin :
    - Il était à l'origine prévu que prendre une pomme (boule rouge), vous fasse mettre dans un état d'invincibilté pour ne pas se faire toucher les fantômes (stégosaures)
    - Les ennemies devaient avoir un déplacement plus complexe, leur donnant la possibilté de changer trajectoire dans le labyrinthe et pas seulement lorsqu'ils rencontent des murs
    - La musique devait être mieux gérée mais ce n'était qu'une partie optionnelle à régler une fois tout le reste terminé