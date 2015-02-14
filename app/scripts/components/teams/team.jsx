var React = require('react');

var Player = require('./player');
var Actions = require('../../actions/team');
var ScoresheetStore = require('../../stores/scoresheet');

var Team = React.createClass({

    getInitialState: function() {
        return {
            new_player: ScoresheetStore.newPlayerDefault()
        };
    },

    nameHandler: function(event) {
        this.setState({
            new_player: {
                name: event.target.value,
                pts: 0,
                team_id: this.props.team.id
            }
        });
    },

    addPlayer: function() {
        var new_player = this.state.new_player;
        this.setState({new_player: ScoresheetStore.newPlayerDefault()});
        Actions.addPlayer({
            team_id: this.props.team.id,
            player: new_player
        });
    },

    render: function() {
        var props = this.props;
        return (
            <div className="row">
                <h5>{this.props.team.name}</h5>
                <div className="col-md-12">
                    <ul>
                        {$.each(this.props.team.players, function (id, player) {
                            return <Player key={id} player={player} team_id={props.team.id} />;
                        })}
                    </ul>
                    <div className="col-md-12">
                        <input type="text" className="form-control" value={this.state.new_player.name} onChange={this.nameHandler} placeholder="Player name..."/>
                        <button type="button" className="btn btn-success" onClick={this.addPlayer}>Add Player</button>
                    </div>
                </div>
            </div>
        );
    }
});

module.exports = Team;
