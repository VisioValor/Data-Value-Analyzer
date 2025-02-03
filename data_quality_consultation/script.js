document.addEventListener("DOMContentLoaded", () => {
    const responses = {};
    let currentTabIndex = 0;
    let currentQuestionIndex = 0;
    const tabNames = Object.keys(tabs);
    const questionContainer = document.getElementById("question-container");
    const sectionTitle = document.getElementById("section-title");
    const questionLabel = document.getElementById("question-label");
    const responseInput = document.getElementById("response-input");
    const nextButton = document.getElementById("next-button");
    const progressBarInner = document.getElementById("progress-bar-inner");
    const resultsDiv = document.getElementById("results");
    const spiderChartCanvas = document.getElementById("spider-chart");

    function updateProgressBar() {
        const currentTab = tabNames[currentTabIndex];
        const totalQuestionsInSection = tabs[currentTab].length;
        const answeredQuestionsInSection = currentQuestionIndex;
        const progressInSection = ((answeredQuestionsInSection / totalQuestionsInSection) * 100).toFixed(2);
        progressBarInner.style.width = `${progressInSection}%`;

        const progressText = document.getElementById("progress-text");
        progressText.textContent = `${answeredQuestionsInSection} / ${totalQuestionsInSection} questions completed in ${currentTab}`;
    }

    function showNextQuestion() {
        const currentTab = tabNames[currentTabIndex];
        const questions = tabs[currentTab];

        if (currentQuestionIndex >= questions.length) {
            if (!responses[currentTab]) {
                responses[currentTab] = {};
            }
            responses[currentTab].answers = responses[currentTab].answers || [];
            responses[currentTab].average = responses[currentTab].answers.reduce((a, b) => a + b, 0) / questions.length;

            currentQuestionIndex = 0;
            currentTabIndex++;

            if (currentTabIndex >= tabNames.length) {
                showResults();
                return;
            }
        }

        const nextTab = tabNames[currentTabIndex];
        const nextQuestion = tabs[nextTab][currentQuestionIndex];

        sectionTitle.textContent = nextTab;
        questionLabel.innerHTML = `<span class="question">${nextQuestion.question}</span><span class="description">${nextQuestion.description}</span>`;
        responseInput.value = "";
        responseInput.focus();

        updateProgressBar();
    }

    function showResults() {
        questionContainer.style.display = "none";
        resultsDiv.style.display = "block";
        resultsDiv.innerHTML = ''; // Clear previous results

        // Create dashboard layout
        resultsDiv.innerHTML = `
            <div class="dashboard">
                <div class="dashboard-header">
                    <h2>Data Value Assessment Dashboard</h2>
                    <div class="total-score-card"></div>
                </div>
                <div class="dashboard-grid">
                    <div class="main-chart">
                        <h3>Overall Assessment</h3>
                        <canvas id="spider-chart"></canvas>
                    </div>
                    <div class="score-table">
                        <h3>Score Breakdown</h3>
                        <div id="score-table-container"></div>
                    </div>
                    <div class="section-charts">
                        <h3>Detailed Section Analysis</h3>
                        <div id="section-charts-container"></div>
                    </div>
                </div>
            </div>
        `;

        const labels = tabNames;
        const data = tabNames.map(tab => responses[tab]?.average || 0);

        // Create the score table
        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Description</th>
                        <th>Weight</th>
                        <th>Rating</th>
                        <th>Weighted Score</th>
                    </tr>
                </thead>
                <tbody>
        `;

        let totalWeightedScore = 0;

        labels.forEach(label => {
            const rating = responses[label]?.average || 0;
            const weight = weights[label];
            const weightedScore = (rating * weight).toFixed(2);
            totalWeightedScore += parseFloat(weightedScore);

            tableHTML += `
                <tr>
                    <td>${label}</td>
                    <td>${(weight * 100).toFixed(0)}%</td>
                    <td>${rating.toFixed(1)}</td>
                    <td>${weightedScore}</td>
                </tr>
            `;
        });

        tableHTML += `
                <tr class="total-row">
                    <td colspan="3"><strong>Total Valuation Score</strong></td>
                    <td><strong>${totalWeightedScore.toFixed(2)}</strong></td>
                </tr>
            </tbody>
        </table>
        `;

        // Add total score card
        const scoreCard = document.querySelector('.total-score-card');
        scoreCard.innerHTML = `
            <div class="score-value">${totalWeightedScore.toFixed(1)}</div>
            <div class="score-label">Total Score</div>
        `;

        // Add score table to container
        document.getElementById('score-table-container').innerHTML = tableHTML;

        // Create the spider chart
        new Chart(document.getElementById('spider-chart'), {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Scores',
                    data: data,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)'
                }]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 10,
                        ticks: {
                            stepSize: 2
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

        // Create section charts container
        const sectionChartsContainer = document.getElementById('section-charts-container');
        
        // Create individual section charts
        labels.forEach(label => {
            const sectionDiv = document.createElement('div');
            sectionDiv.className = 'section-chart';
            sectionDiv.innerHTML = `
                <h4>${label}</h4>
                <canvas id="chart-${label.toLowerCase().replace(/\s+/g, '-')}"></canvas>
            `;
            sectionChartsContainer.appendChild(sectionDiv);

            const questions = tabs[label];
            const questionLabels = questions.map((q, idx) => `Q${idx + 1}`);
            const questionScores = responses[label]?.answers || Array(questions.length).fill(0);

            new Chart(sectionDiv.querySelector('canvas'), {
                type: 'bar',
                data: {
                    labels: questionLabels,
                    datasets: [{
                        label: 'Question Scores',
                        data: questionScores,
                        backgroundColor: 'rgba(54, 162, 235, 0.6)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10,
                            ticks: {
                                stepSize: 2
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                title: function(context) {
                                    const idx = context[0].dataIndex;
                                    return questions[idx].question;
                                }
                            }
                        }
                    }
                }
            });
        });

        // Add download button
        const downloadButton = document.createElement('button');
        downloadButton.textContent = 'Download Report';
        downloadButton.className = 'download-button';
        downloadButton.addEventListener('click', downloadReport);
        resultsDiv.appendChild(downloadButton);
    }

    function downloadReport() {
        // Create a temporary container for PDF content
        const pdfContainer = document.createElement('div');
        pdfContainer.style.position = 'absolute';
        pdfContainer.style.left = '-9999px';
        document.body.appendChild(pdfContainer);

        // Create content for PDF
        const content = `
            <div style="padding: 20px; font-family: Arial, sans-serif;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50; margin: 0; padding: 20px 0; border-bottom: 2px solid #2c3e50;">
                        VisioValor Data Valuation Report
                    </h1>
                </div>

                <div style="margin-bottom: 40px;">
                    <h2 style="color: #2c3e50;">Summary</h2>
                    ${resultsDiv.querySelector('table').outerHTML}
                </div>

                <div style="margin-bottom: 40px; page-break-before: always;">
                    <h2 style="color: #2c3e50;">Visualization</h2>
                    <canvas id="pdf-chart" width="600" height="400" style="max-width: 100%;"></canvas>
                </div>

                <div style="page-break-before: always;">
                    <h2 style="color: #2c3e50;">Detailed Responses</h2>
                    ${resultsDiv.querySelectorAll('table')[1].outerHTML}
                </div>

                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 10px; color: #666;">
                    The questions, methodology, and output contained within this report remain the exclusive property of VisioValor. 
                    Unauthorized reproduction, distribution, or use of any part of this report without prior written consent from VisioValor is strictly prohibited.
                </div>
            </div>
        `;

        pdfContainer.innerHTML = content;

        // Style all tables in the PDF
        pdfContainer.querySelectorAll('table').forEach(table => {
            table.style.width = '100%';
            table.style.borderCollapse = 'collapse';
            table.style.marginBottom = '20px';
            
            table.querySelectorAll('th, td').forEach(cell => {
                cell.style.border = '1px solid #ddd';
                cell.style.padding = '8px';
                cell.style.textAlign = 'left';
            });

            table.querySelectorAll('th').forEach(th => {
                th.style.backgroundColor = '#f2f2f2';
            });
        });

        // Create a new chart on the PDF canvas
        const pdfChart = new Chart(pdfContainer.querySelector('#pdf-chart'), {
            type: 'radar',
            data: {
                labels: tabNames,
                datasets: [{
                    label: 'Scores',
                    data: tabNames.map(tab => responses[tab]?.average || 0),
                    backgroundColor: 'rgba(44, 62, 80, 0.2)',
                    borderColor: 'rgba(44, 62, 80, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true,
                        max: 10
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                animation: {
                    duration: 0 // Disable animation for PDF
                }
            }
        });

        // Wait for chart to render
        setTimeout(() => {
            // Configure PDF options
            const opt = {
                margin: 20,
                filename: 'VisioValor_Data_Valuation_Report.pdf',
                image: { type: 'jpeg', quality: 1 },
                html2canvas: { 
                    scale: 2,
                    useCORS: true,
                    logging: false,
                    backgroundColor: '#ffffff'
                },
                jsPDF: { 
                    unit: 'mm', 
                    format: 'a4', 
                    orientation: 'portrait'
                },
                pagebreak: { 
                    mode: ['avoid-all', 'css', 'legacy'],
                    before: '[style*="page-break-before: always"]'
                }
            };

            // Generate and download PDF
            html2pdf()
                .from(pdfContainer)
                .set(opt)
                .save()
                .then(() => {
                    pdfChart.destroy(); // Clean up chart
                    document.body.removeChild(pdfContainer);
                })
                .catch(error => {
                    console.error('Error generating PDF:', error);
                    pdfChart.destroy(); // Clean up chart
                    document.body.removeChild(pdfContainer);
                });
        }, 500); // Wait for 500ms to ensure chart is rendered
    }

    nextButton.addEventListener("click", () => {
        const currentTab = tabNames[currentTabIndex];
        const inputValue = Number(responseInput.value);

        if (!inputValue || inputValue < 1 || inputValue > 10) {
            alert("Please enter a value between 1 and 10.");
            return;
        }

        if (!responses[currentTab]) {
            responses[currentTab] = {
                answers: []
            };
        }

        responses[currentTab].answers.push(inputValue);
        currentQuestionIndex++;
        showNextQuestion();
    });

    responseInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            nextButton.click();
        }
    });

    showNextQuestion();
}); 