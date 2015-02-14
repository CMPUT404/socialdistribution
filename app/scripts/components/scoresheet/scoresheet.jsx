var React = require('react');
var Reflux = require('reflux');
var Team = require('../teams/team');
var ScoresheetStore = require('../../stores/scoresheet');
var SheetActions = require('../../actions/scoresheet');
var TimeToggler = require('./timetoggler');

var Scoresheet = React.createClass({

  mixins: [Reflux.connect(ScoresheetStore)],

  getInitialState: function() {
      return {
          teams: ScoresheetStore.getInitialTeams()
      };
  },

  render: function() {

    var homeTeam;
    var awayTeam;
    var homeComponent;
    var awayComponent;

    var tKeys = Object.keys(this.state.teams);
    if (tKeys.length > 0) {
        homeTeam = this.state.teams[tKeys[0]];
        homeComponent = <Team team={homeTeam} />;
    }
    if (tKeys.length > 1) {
        awayTeam = this.state.teams[tKeys[1]];
        awayComponent = <Team team={awayTeam} />;
    }

    return (
      <div className="scoresheet">
        <div className="row context">
          <div className="col-sm-4">
            <h3 className="text-center">Home: {homeTeam.score}</h3>
          </div>
          <div className="col-sm-4">
            <TimeToggler time={this.state.time} running={this.state.running} onClick={SheetActions.triggerTimer} />
          </div>
          <div className="col-sm-4">
            <h3 className="text-center">Away: {awayTeam.score}</h3>
          </div>
        </div>

        <div className="row scoresheet">
          <div className="col-sm-6 home-sheet">
            {homeComponent}
          </div>
          <div className="col-sm-6 away-sheet">
            {awayComponent}
          </div>
        </div>
      </div>
    );
  }
});

module.exports = Scoresheet;
