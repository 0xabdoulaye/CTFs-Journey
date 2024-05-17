## Docker Network
La commande `docker network` est la commande principale pour configurer et gérer les réseaux de conteneurs. Exécutez la commande docker network à partir du premier terminal.

```sh
$ docker network 

Usage:  docker network COMMAND

Manage networks

Commands:
  connect     Connect a container to a network
  create      Create a network
  disconnect  Disconnect a container from a network
  inspect     Display detailed information on one or more networks
  ls          List networks
  prune       Remove all unused networks
  rm          Remove one or more networks

$ docker network  ls
NETWORK ID     NAME      DRIVER    SCOPE
5d60c85ff790   bridge    bridge    local
925b64d887e8   host      host      local
7893bf28e568   none      null      local
[node1] (local) root@192.168.0.28 ~
```
La sortie ci-dessus montre les réseaux de conteneurs qui sont créés dans le cadre d'une installation standard de Docker.
Les nouveaux réseaux que vous créez apparaîtront également dans la sortie de la commande docker network ls.
Vous pouvez voir que chaque réseau reçoit un ID et un NAME uniques. Chaque réseau est également associé à un pilote unique. Remarquez que le réseau "bridge" et le réseau "host" ont le même nom que leurs pilotes respectifs.