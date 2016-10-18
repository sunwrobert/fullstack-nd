# Tournament Results Planner

This project provides a python module that connects to a PostgresSQL database in order to keep track of players and their matches against other players. The functionalities of the python module include adding players, deleting players, reporting matches, and calculating the Swiss pairings of the tournament based on the current match records of each player.

## How to Run

This project requires Vagrant to run, which can be downloaded here: https://www.vagrantup.com/
1. `git clone https://github.com/sunwrobert/fullstack-nd.git`
2. `cd projects/tournament-results/vagrant`
3. `vagrant up`
4. `vagrant ssh`
5. `cd /vagrant/tournament`
6. Test with `python tournament_test.py`
