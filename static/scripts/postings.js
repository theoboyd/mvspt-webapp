function smartColumns() {
  // Create a function that calculates the smart columns
  // Reset column size to a 100% once view port has been adjusted
	$("ul.column").css({ 'width' : "100%"});

  // Get the width of row
	var colWrap = $("ul.column").width();

  // Find how many columns of this width can fit per row then round it down to a
  // whole number
	var colNum = Math.floor(colWrap / 400);

  // Get the width of the row and divide it by the number of columns it can fit
  // then round it down to a whole number. This value will be the exact width of
  // the re-adjusted column
	var colFixed = Math.floor(colWrap / colNum);

  // Set exact width of row in pixels instead of using % - Prevents
  // cross-browser bugs that appear in certain view port resolutions
	$("ul.column").css({ 'width' : colWrap});

  // Set exact width of the re-adjusted column	
	$("ul.column li").css({ 'width' : colFixed});
}	

// Execute the function when page loads
smartColumns();

$(window).resize(function () {
  // Each time the viewport is adjusted/resized, execute the function
	smartColumns();
});
