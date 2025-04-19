document.addEventListener('DOMContentLoaded', function () {
  // Event listener for adding investment fields
  document.getElementById('addInvestmentsBtn').addEventListener('click', function () {
    addInvestmentFields();
  });

  // Event listener for calculating returns
  document.getElementById('calculateBtn').addEventListener('click', function () {
    calculateReturns();
  });
});

function addInvestmentFields() {
  const numInvestments = document.getElementById('numInvestments').value;
  const investmentFieldsContainer = document.getElementById('investmentFields');

  investmentFieldsContainer.innerHTML = ''; // Clear existing fields

  if (numInvestments <= 0) {
    alert('Please enter a valid number of investments.');
    return;
  }

  for (let i = 0; i < numInvestments; i++) {
    const costInput = document.createElement('input');
    costInput.type = 'number';
    costInput.placeholder = `Investment ${i + 1} - Cost`;
    costInput.id = `cost_${i}`; // Set unique id for each input

    const returnInput = document.createElement('input');
    returnInput.type = 'number';
    returnInput.placeholder = `Investment ${i + 1} - Return`;
    returnInput.id = `return_${i}`; // Set unique id for each input

    investmentFieldsContainer.appendChild(costInput);
    investmentFieldsContainer.appendChild(returnInput);
    investmentFieldsContainer.appendChild(document.createElement('br')); // Add line break between fields
  }
}

function calculateReturns() {
  const budget = parseFloat(document.getElementById('budget').value);
  if (isNaN(budget) || budget <= 0) {
    alert('Please enter a valid budget.');
    return;
  }

  const investments = [];
  const numInvestments = document.getElementById('numInvestments').value;

  for (let i = 0; i < numInvestments; i++) {
    const cost = parseFloat(document.getElementById(`cost_${i}`).value);
    const returns = parseFloat(document.getElementById(`return_${i}`).value);

    if (isNaN(cost) || isNaN(returns) || cost <= 0 || returns <= 0) {
      alert('Please enter valid cost and return values for all investments.');
      return;
    }

    investments.push([cost, returns]);
  }

  const result = fractionalKnapsack(budget, investments);

  // Debugging output to the console
  console.log('Investments:', investments);
  console.log('Calculated result:', result);

  // Ensure results div is visible
  const resultsDiv = document.getElementById('resultsText');
  resultsDiv.style.display = 'block';
  resultsDiv.textContent = `Maximum Return: ${result.totalReturns.toFixed(2)}\n\n${result.breakdown.join('\n')}`;

  plotComparison(result.totalReturns);
}

function fractionalKnapsack(budget, investments) {
  investments.sort((a, b) => (b[1] / b[0]) - (a[1] / a[0])); // Sort by return per cost ratio
  let totalReturns = 0;
  let breakdown = [];

  for (let [cost, returns] of investments) {
    if (budget >= cost) {
      budget -= cost;
      totalReturns += returns;
      breakdown.push(`Included 100% of investment with cost ${cost} and return ${returns}`);
    } else {
      totalReturns += (returns * (budget / cost));
      breakdown.push(`Included ${(budget / cost * 100).toFixed(2)}% of investment with cost ${cost} and return ${returns}`);
      break;
    }
  }

  return { totalReturns, breakdown };
}

function plotComparison(currentReturn) {
  const historicalReturns = [500, 1000, 1500]; // Example historical data
  const averageHistoricalReturn = historicalReturns.length > 0 ? historicalReturns.reduce((a, b) => a + b, 0) / historicalReturns.length : 0;

  const ctx = document.getElementById('comparisonChart').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Current Return', 'Average Historical Return'],
      datasets: [{
        label: 'Returns',
        data: [currentReturn, averageHistoricalReturn],
        backgroundColor: ['#00c853', '#ff7043'],
        borderColor: ['#00c853', '#ff7043'],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) { return '$' + value; }
          }
        }
      }
    }
  });
}
