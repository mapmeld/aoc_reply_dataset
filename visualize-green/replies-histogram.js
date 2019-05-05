fetch('all-environment.json')
  .then(res => res.json())
  .then((data) => {
    fetch('origin-environment.json')
      .then(res => res.json())
      .then((aoctweets) => {
        const svg = d3.select('#chart');

        let bins = [];
        data.forEach((tstamp) => {
          let dt = new Date(tstamp * 1000);
          if (dt.getFullYear() === 2019 && dt.getMonth() === 2) {
            // March 2019
            let dayOfMonth = dt.getDate() - 1;
            let histogramCursor = 6 * dayOfMonth + Math.floor(dt.getHours() / 4);
            while (typeof bins[histogramCursor] !== 'object') {
              bins.push([]);
            }
            bins[histogramCursor].push(tstamp);
          }
        });
        // console.log(bins);

        const x = d3.scaleLinear()
          .domain([0, 31 * 6])
          .range([10, 890]);
        const y = d3.scaleLinear()
          .domain([0, 200]).nice()
          .range([340, 10]);

        const bar = svg.append("g")
          .attr("fill", "steelblue")
          .selectAll("rect")
          .data(bins)
          .join("rect")
            .attr("x", (d, i) => x(i))
            .attr("width", x(1) / 5.5)
            .attr("y", d => y(d.length))
            .attr("height", d => y(0) - y(d.length));

        aoctweets = aoctweets.map((tweet) => {
          if (tweet) {
            let revv = tweet.split(' - ').reverse().join(' ');
            //console.log(revv);
            // Pacific to Eastern
            return new Date(new Date(revv) * 1 + (3 * 60 * 60 * 1000));
          }
        })
        .filter(dt => dt && (dt.getFullYear() === 2019 && dt.getMonth() === 2));

        aoctweets = aoctweets.map((dt) => {
          let dayOfMonth = dt.getDate() - 1;
          let histogramCursor = 6 * dayOfMonth + Math.floor(dt.getHours() / 4);
          svg.append('rect')
            .attr('fill', 'orangered')
            .attr('x', x(histogramCursor))
            .attr('y', y(bins[histogramCursor].length) + 10)
            .attr('width', x(1) / 7)
            .attr('height', 330 - y(bins[histogramCursor].length));
        });

        xAxis = g => g
          .attr("transform", `translate(0,340)`)
          .call(d3.axisBottom(x).tickSizeOuter(0).ticks(10));

        svg.append("g")
            .call(xAxis);

        let ticks = d3.selectAll('.tick text')._groups[0];
        for (var v = 0; v < ticks.length; v++) {
          ticks[v].textContent = Math.floor(ticks[v].textContent * 1 / 6) + 1;
        }

        return svg.node();
      });
  });
