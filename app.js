(function() {
  "use strict";
  /*************************** Variables ******************************/
  /**
   * The starting point in our program, setting up a listener
   * for the "load" event on the window. When this event occurs,
   * the attached function (initialize) will be called.
   */
  window.addEventListener("load", initialize);


  function initialize() {
    $('Generate-Button').addEventListener('click', function() {
      let input = document.querySelectorAll('input');
      let totalTAs = input[input.length - 1].value * input[input.length - 2].value;
      console.log("total TAs: " + totalTAs);
      let students = [];
      for (let i = 0; i < input.length - 2; i++) {
        students.push(input[i].value);
      }
      console.log("Student Populations: " + students);
      let distribution = jefferson(students, totalTAs);
      console.log("distribution: " + distribution)
      generateOutput(distribution);
    });
  }

  function generateOutput(distribution) {
    let table = $("Answer-Table");
    table.innerText = "";
    table.appendChild($("Input-Table").cloneNode(true));
    let answer = document.querySelectorAll('#Input-Table')[1].childNodes;

    let rows = [];
    for (let i = 3; i < answer.length; i += 2) {
      rows.push(answer[i].childNodes);
    }
    console.log(rows);
    for (let i = 0; i < rows.length; i++) {
      for (let j = 3; j < rows[i].length; j++) {
        let index = i * 7 + Math.floor(j / 2) - 1;
        rows[i][j].innerText = distribution[index] === 0 ? "" : distribution[index];
      }
    }
    
    document.querySelectorAll('#Special-Box')[1].innerText = "Output Table";

  }

  /**
   * Uses Jefferson's Method to apportion the TAs.
   * @param {int} tas - Number of total TA hours.
   * @param {Array} studentDistr - The raw student values as an array.
   * @returns {Array} with the number of integer TAs in the corresponding slots.
   */
  function jefferson(studentDistr, tas) {
    let totalStudents = sum(studentDistr);
    let stdDivisor = totalStudents / tas;
    console.log("Standard Divisor: " + stdDivisor);
    let exactQuotas = getQuotas(studentDistr, stdDivisor);
    console.log(exactQuotas);
    let result = arrayFloor(exactQuotas);
    console.log(result);
    let total = sum(result);
    console.log(total);
    let stepSize = totalStudents / 10000;
    while (total < tas) {
      stdDivisor -= stepSize;
      exactQuotas = getQuotas(studentDistr, stdDivisor);
      result = arrayFloor(exactQuotas);
      total = sum(result);
      console.log("result: " + result);
      console.log("total: " + total);
    }
    return result;
  }

  /**
   * Takes a student distribution and std divisor and returns the Array
   * with the quotas calculated using those values.
   */
  function getQuotas(studentDistr, stdDivisor) {
    let result = [];
    for (let i = 0; i < studentDistr.length; i++) {
      result.push(studentDistr[i] === 0 ? null : studentDistr[i] / stdDivisor);
    }
    return result;
  }

  /**
   * Floors each value in array. If value is null, the output value at the
   * corresponding index are null.
   */
  function arrayFloor(array) {
    let result = [];
    for (let i = 0; i < array.length; i++) {
      result.push(array[i] === null ? null : Math.floor(array[i]));
    }
    return result;
  }

  /**
   * Returns the sum over array.
   * @param {int[]} array
   * @returns {int} sum over the array.
   */
  function sum(array) {
    let total = 0;
    for (let i = 0; i < array.length; i++) {
        total += Number(array[i]);
    }
    return total;
  }

  /**
   * Helper function for shortening getElementById.
   * @param {String} id - Id.
   */
  function $(id) {
    return document.getElementById(id);
  }

})();
