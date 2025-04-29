
  // DOM elements
  const homeTeamList = document.getElementById('home-team-list');
  const awayTeamList = document.getElementById('away-team-list');
  const predictButton = document.getElementById('predict-button');
  const resultsContainer = document.getElementById('results-container');
  const matchTitle = document.getElementById('match-title');

  // Team name elements
  const homeTeamNameH2h = document.getElementById('home-team-name-h2h');
  const awayTeamNameH2h = document.getElementById('away-team-name-h2h');
  const homeTeamNamePred = document.getElementById('home-team-name-pred');
  const awayTeamNamePred = document.getElementById('away-team-name-pred');
  const homeTeamNameForm = document.getElementById('home-team-name-form');
  const awayTeamNameForm = document.getElementById('away-team-name-form');

  // Selected teams
  let selectedHomeTeam = null;
  let selectedAwayTeam = null;

  // Match data (would come from an API in a real application)
  const matchData = {
  'Benfica-Manchester United': {
  headToHead: {
  totalMatches: 13,
  homeWins: 0,
  awayWins: 8,
  draws: 0
},
  lastMatch: {
  date: '2023-11-15',
  score: '2 - 1',
  winner: 'Manchester United'
},
  prediction: {
  homeWin: 33,
  awayWin: 22,
  draw: 45
},
  teamForm: {
  home: ['D', 'W', 'L', 'W', 'D'],
  away: ['D', 'L', 'L', 'W', 'W']
},
  keyStats: {
  possession: {
  home: 52,
  away: 48
},
  shotsOnTarget: {
  home: 8,
  away: 7
},
  yellowCards: {
  home: 5,
  away: 3
}
}
}
};

  // Generate random match data for any team combination
  function generateRandomMatchData(homeTeam, awayTeam) {
  const homeWins = Math.floor(Math.random() * 10);
  const awayWins = Math.floor(Math.random() * 10);
  const draws = Math.floor(Math.random() * 5);
  const totalMatches = homeWins + awayWins + draws;

  const homeWinProb = Math.floor(Math.random() * 40) + 20;
  const awayWinProb = Math.floor(Math.random() * 40) + 20;
  const drawProb = 100 - homeWinProb - awayWinProb;

  const homePossession = Math.floor(Math.random() * 30) + 35;
  const awayPossession = 100 - homePossession;

  const homeShots = Math.floor(Math.random() * 10) + 3;
  const awayShots = Math.floor(Math.random() * 10) + 3;

  const homeCards = Math.floor(Math.random() * 6) + 1;
  const awayCards = Math.floor(Math.random() * 6) + 1;

  const formOptions = ['W', 'L', 'D'];
  const homeForm = Array.from({length: 5}, () => formOptions[Math.floor(Math.random() * formOptions.length)]);
  const awayForm = Array.from({length: 5}, () => formOptions[Math.floor(Math.random() * formOptions.length)]);

  // Generate a random score
  const homeScore = Math.floor(Math.random() * 4);
  const awayScore = Math.floor(Math.random() * 4);
  let winner = homeScore > awayScore ? homeTeam : (awayScore > homeScore ? awayTeam : 'Draw');

  // Generate a random date in the last 60 days
  const date = new Date();
  date.setDate(date.getDate() - Math.floor(Math.random() * 60));
  const formattedDate = date.toISOString().split('T')[0];

  return {
  headToHead: {
  totalMatches,
  homeWins,
  awayWins,
  draws
},
  lastMatch: {
  date: formattedDate,
  score: `${homeScore} - ${awayScore}`,
  winner
},
  prediction: {
  homeWin: homeWinProb,
  awayWin: awayWinProb,
  draw: drawProb
},
  teamForm: {
  home: homeForm,
  away: awayForm
},
  keyStats: {
  possession: {
  home: homePossession,
  away: awayPossession
},
  shotsOnTarget: {
  home: homeShots,
  away: awayShots
},
  yellowCards: {
  home: homeCards,
  away: awayCards
}
}
};
}

  // Handle team selection
  function handleTeamSelection(listElement, isHomeTeam) {
  const teamItems = listElement.querySelectorAll('.team-item');

  teamItems.forEach(item => {
  item.addEventListener('click', () => {
  // Remove selected class from all items in this list
  teamItems.forEach(i => i.classList.remove('selected'));

  // Add selected class to clicked item
  item.classList.add('selected');

  // Update selected team
  const teamName = item.dataset.team;

  if (isHomeTeam) {
  selectedHomeTeam = teamName;
} else {
  selectedAwayTeam = teamName;
}

  // Enable predict button if both teams are selected
  predictButton.disabled = !(selectedHomeTeam && selectedAwayTeam);
});
});
}

  // Display match statistics
  function displayMatchStats(homeTeam, awayTeam) {
  // Update match title
  matchTitle.textContent = `${homeTeam} vs ${awayTeam}`;

  // Update team names in all sections
  homeTeamNameH2h.textContent = homeTeam;
  awayTeamNameH2h.textContent = awayTeam;
  homeTeamNamePred.textContent = homeTeam;
  awayTeamNamePred.textContent = awayTeam;
  homeTeamNameForm.textContent = homeTeam;
  awayTeamNameForm.textContent = awayTeam;

  // Get match data (either from predefined data or generate random)
  const matchKey = `${homeTeam}-${awayTeam}`;
  const data = matchData[matchKey] || generateRandomMatchData(homeTeam, awayTeam);

  // Update head to head stats
  document.getElementById('total-matches').textContent = data.headToHead.totalMatches;
  document.getElementById('home-wins').textContent = data.headToHead.homeWins;
  document.getElementById('away-wins').textContent = data.headToHead.awayWins;
  document.getElementById('draws').textContent = data.headToHead.draws;

  // Update last match stats
  document.getElementById('last-match-date').textContent = data.lastMatch.date;
  document.getElementById('last-match-score').textContent = data.lastMatch.score;
  document.getElementById('last-match-winner').textContent = data.lastMatch.winner;

  // Update prediction stats
  document.getElementById('home-win-percentage').textContent = `${data.prediction.homeWin}%`;
  document.getElementById('away-win-percentage').textContent = `${data.prediction.awayWin}%`;
  document.getElementById('draw-percentage').textContent = `${data.prediction.draw}%`;

  document.getElementById('home-win-bar').style.width = `${data.prediction.homeWin}%`;
  document.getElementById('away-win-bar').style.width = `${data.prediction.awayWin}%`;
  document.getElementById('draw-bar').style.width = `${data.prediction.draw}%`;

  // Update team form
  const homeTeamForm = document.getElementById('home-team-form');
  const awayTeamForm = document.getElementById('away-team-form');

  homeTeamForm.innerHTML = '';
  awayTeamForm.innerHTML = '';

  data.teamForm.home.forEach(result => {
  const indicator = document.createElement('div');
  indicator.className = `form-indicator form-${result.toLowerCase()}`;
  indicator.textContent = result;
  homeTeamForm.appendChild(indicator);
});

  data.teamForm.away.forEach(result => {
  const indicator = document.createElement('div');
  indicator.className = `form-indicator form-${result.toLowerCase()}`;
  indicator.textContent = result;
  awayTeamForm.appendChild(indicator);
});

  // Update key stats
  document.getElementById('home-possession').textContent = `${data.keyStats.possession.home}%`;
  document.getElementById('away-possession').textContent = `${data.keyStats.possession.away}%`;
  document.getElementById('home-shots').textContent = data.keyStats.shotsOnTarget.home;
  document.getElementById('away-shots').textContent = data.keyStats.shotsOnTarget.away;
  document.getElementById('home-cards').textContent = data.keyStats.yellowCards.home;
  document.getElementById('away-cards').textContent = data.keyStats.yellowCards.away;

  document.getElementById('home-possession-bar').style.width = `${data.keyStats.possession.home}%`;
  document.getElementById('away-possession-bar').style.width = `${data.keyStats.possession.away}%`;

  const totalShots = data.keyStats.shotsOnTarget.home + data.keyStats.shotsOnTarget.away;
  const homeShotsPercentage = (data.keyStats.shotsOnTarget.home / totalShots) * 100;
  const awayShotsPercentage = (data.keyStats.shotsOnTarget.away / totalShots) * 100;

  document.getElementById('home-shots-bar').style.width = `${homeShotsPercentage}%`;
  document.getElementById('away-shots-bar').style.width = `${awayShotsPercentage}%`;

  const totalCards = data.keyStats.yellowCards.home + data.keyStats.yellowCards.away;
  const homeCardsPercentage = (data.keyStats.yellowCards.home / totalCards) * 100;
  const awayCardsPercentage = (data.keyStats.yellowCards.away / totalCards) * 100;

  document.getElementById('home-cards-bar').style.width = `${homeCardsPercentage}%`;
  document.getElementById('away-cards-bar').style.width = `${awayCardsPercentage}%`;

  // Show results container
  resultsContainer.style.display = 'block';
}

  // Initialize
  handleTeamSelection(homeTeamList, true);
  handleTeamSelection(awayTeamList, false);

  // Add event listener to predict button
  predictButton.addEventListener('click', () => {
  if (selectedHomeTeam && selectedAwayTeam) {
  displayMatchStats(selectedHomeTeam, selectedAwayTeam);
}
});

  // Pre-select Benfica and Manchester United for demonstration
  document.querySelector('#home-team-list [data-team="Benfica"]').click();
  document.querySelector('#away-team-list [data-team="Manchester United"]').click();
