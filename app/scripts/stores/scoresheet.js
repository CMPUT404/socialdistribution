var Reflux = require('reflux');

var SheetActions = require('../actions/scoresheet');
var TeamActions = require('../actions/team');

// Deals with App State Machine state
var ScoresheetStore = Reflux.createStore({

    // Tracks our timer when it's running so we know where to stop it
    timer_id: '',

    // how fast to decrement our clock in seconds
    timer_increment: 0.50,

    init: function() {

        // Listeners
        this.listenTo(SheetActions.triggerTimer, this.toggleTime);
        this.listenTo(SheetActions.timerTick, this.decrementTime);
        this.listenTo(TeamActions.updateScore, this.updateScore);
        this.listenTo(TeamActions.addPlayer, this.updateTeamPlayer);

        // initialize data
        this.teams = this.getInitialTeams();
    },

    // Handles starting and stopping the game clock
    toggleTime: function() {
        // Flip State
        this.scoreboard.running = !this.scoreboard.running;

        if (this.scoreboard.running) {
            this.timer_id = setInterval(BoardActions.timerTick, this.timer_increment * 1000)
        } else {
            clearInterval(this.timer_id);
        }

        this.trigger({running: this.scoreboard.running});
    },

    // Handles updating game clock settings
    decrementTime: function() {
        this.scoreboard.time -= this.timer_increment;
        this.trigger({time: this.scoreboard.time});
    },

    // Handles changes in score
    updateScore: function (result) {
        this.teams[result.team_id].score += result.points;
        this.updateTeamPlayer(result.team_id, result.player);
        this.trigger({teams: this.teams});
    },

    getInitialTeams: function() {
        var teams = {};
        for(i = 0; i < 2; i++) {
            var newTeam = this.newDefaultTeam();
            teams[newTeam.id] = newTeam;
        }
        return teams;
    },

    // TODO: Convert this into class constructor
    newDefaultTeam: function(id) {
        var testPlayer = this.newPlayerDefault();
        var players = {};
        players[testPlayer.id] = testPlayer;

        return {
            id: Math.random(),
            players: players,
            score: 0
        };
    },

    // TODO: Convert this into class constructor
    newPlayerDefault: function () {
        return {
            id: Math.random(), // ghetto UUID
            name: '',
            points: 0,
        };
    },

    // TODO: make this a Team class call
    // Simply needs to update the player
    updateTeamPlayer: function (team_id, player) {
        this.teams[team_id].players[result.player.id] = result.player;
    },
});

module.exports = ScoresheetStore;
