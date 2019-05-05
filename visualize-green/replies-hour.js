fetch('replies-by-tstamp.json')
  .then(res => res.json())
  .then((data) => {
    let tweets = Object.keys(data.green);
    let minutes = [];
    tweets.forEach((tweet) => {
      if (data.green[tweet].length) {
        let zeroHour = data.green[tweet][0] - 1;
        data.green[tweet].forEach((time) => {
          let minuteTime = Math.ceil((time - zeroHour) / 30);
          while (minutes.length < minuteTime) {
            minutes.push(0);
          }
          minutes[minuteTime - 1]++;
        });
      }
    });
    // console.log(minutes);

    let badminutes = [];
    tweets.forEach((tweet) => {
      if (data.bad[tweet].length) {
        let zeroHour = data.bad[tweet][0] - 1;
        data.bad[tweet].forEach((time) => {
          let minuteTime = Math.ceil((time - zeroHour) / 30);
          console.log(minuteTime);
          while (badminutes.length < minuteTime) {
            badminutes.push(0);
          }
          badminutes[minuteTime - 1]++;
        });
      }
    });
    console.log(badminutes);

    const svg = d3.select('#chart');
    const x = d3.scaleLinear()
      .domain([0, 180])
      .range([10, 890]);
    const y = d3.scaleLinear()
      .domain([0, 140]).nice()
      .range([340, 10]);

    const bar = svg.append("g")
      .selectAll("rect")
      .data(minutes.slice(0, 180).concat(badminutes.slice(0, 180)))
      .join("rect")
        .attr("x", (d, i) => x(i % 180))
        .attr("fill", (d, i) => (i >= 180) ? 'orange' : 'darkgreen')
        .attr("width", x(1) / 4)
        .attr("y", (d, i) => (i >= 180) ? y(d + minutes[i - 180]) : y(d))
        .attr("height", d => y(0) - y(d));
  });
