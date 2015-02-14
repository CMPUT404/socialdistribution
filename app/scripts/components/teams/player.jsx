var React = require('react');

var Actions = require('../../actions/team');

var Player = React.createClass({

    // handles building the data within the updateScore action
    buildUpdateScore: function(points) {
        this.props.player.points += points;
        return {
            team_id: this.props.team_id,
            player: this.props.player,
            points: points
        };
    },

    add1Point: function() {
        Actions.updateScore(this.buildUpdateScore(1));
    },

    add2Point: function() {
        Actions.updateScore(this.buildUpdateScore(2));
    },

    add3Point: function() {
        Actions.updateScore(this.buildUpdateScore(3));
    },

    render: function() {
        return (
            <li>
                <div>
                    <span>Name: {this.props.player.name}</span>
                    <span>Points: {this.props.player.points}</span>
                    <button type="button" className="btn btn-success point-adder" onClick={this.add1Point}>1</button>
                    <button type="button" className="btn btn-success point-adder" onClick={this.add2Point}>2</button>
                    <button type="button" className="btn btn-success point-adder" onClick={this.add3Point}>3</button>
                </div>
            </li>
        );
    }
});

module.exports = Player;
