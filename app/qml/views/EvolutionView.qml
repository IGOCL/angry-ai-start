import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    Layout.fillWidth: true
    Layout.fillHeight: true

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            ChartPanel { Layout.fillWidth: true; Layout.preferredHeight: 260; title: "Generation Fitness Timeline"; series: appState.fitnessSeries; lineColor: "#46C3FF" }
            Rectangle {
                Layout.preferredWidth: 280
                Layout.fillHeight: true
                radius: 12
                color: "#111A29"
                border.color: "#1B2A41"
                Column {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 8
                    Label { text: "Evolution Diagnostics"; color: "#D9E9FF"; font.bold: true }
                    Label { text: "Diversity: dynamic"; color: "#A1C7EB" }
                    Label { text: "Exploration: adaptive"; color: "#A1C7EB" }
                    Label { text: "Mutation tiers: active"; color: "#A1C7EB" }
                    Label { text: "Stagnation guard: on"; color: "#A1C7EB" }
                    Label { text: "Gen " + appState.currentGeneration + " / " + appState.totalGenerations; color: "#8FD3FF"; font.bold: true }
                    Label { text: "Chunk " + (appState.currentChunk > 0 ? appState.currentChunk : "n/a") + " / " + (appState.totalChunks > 0 ? appState.totalChunks : "n/a"); color: "#A1C7EB" }
                    Label { text: "Candidate " + (appState.currentCandidate > 0 ? appState.currentCandidate : "n/a") + " / " + (appState.totalCandidates > 0 ? appState.totalCandidates : "n/a"); color: "#A1C7EB" }
                    Label { text: "Rows Processed: " + (appState.rowsProcessedLive > 0 ? appState.rowsProcessedLive : "n/a"); color: "#A1C7EB" }
                    Label { text: "Active Template: " + (appState.activeTemplateName && appState.activeTemplateName.length > 0 ? appState.activeTemplateName : "n/a"); color: "#A1C7EB" }
                    Label { text: "Candidates: " + appState.candidateCount; color: "#A1C7EB" }
                    Label { text: "Evaluated: " + appState.evaluatedCount; color: "#A1C7EB" }
                    Label { text: "Survived: " + appState.survivedCount; color: "#A1C7EB" }
                    Label { text: "Rejected: " + appState.rejectedCount; color: "#A1C7EB" }
                    Label { text: "Source Rows: " + (appState.sourceTotalRows > 0 ? appState.sourceTotalRows : "n/a"); color: "#A1C7EB" }
                    Label { text: "Loaded Rows: " + (appState.loadedRows > 0 ? appState.loadedRows : "n/a"); color: "#A1C7EB" }
                    Label { text: "Feature Rows: " + (appState.featureRows > 0 ? appState.featureRows : "n/a"); color: "#A1C7EB" }
                    Label { text: "Research Rows: " + (appState.researchRows > 0 ? appState.researchRows : "n/a"); color: "#A1C7EB" }
                    Label { text: "Source TF: " + (appState.sourceTimeframeLabel && appState.sourceTimeframeLabel.length > 0 ? appState.sourceTimeframeLabel : "n/a"); color: "#A1C7EB" }
                    Label { text: "Research TF: " + (appState.researchTimeframeLabel && appState.researchTimeframeLabel.length > 0 ? appState.researchTimeframeLabel : "n/a"); color: "#A1C7EB" }
                    Label { text: "Executed Trades: " + (appState.executedTrades >= 0 ? appState.executedTrades : "n/a"); color: "#A1C7EB" }
                    Label { text: "Best Score: " + Number(appState.bestScore).toFixed(2); color: "#8FD3FF"; font.bold: true }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 12
            color: "#0F1725"
            border.color: "#1B2A41"
            ListView {
                anchors.fill: parent
                anchors.margins: 10
                model: appState.logs
                delegate: Label {
                    required property var modelData
                    text: modelData.msg
                    color: "#9EC0E3"
                }
                ScrollBar.vertical: ScrollBar {}
            }
        }
    }
}
