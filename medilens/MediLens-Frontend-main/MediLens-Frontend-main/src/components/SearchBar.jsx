function SearchBar({ onSearch }) {
  const handleSearch = () => {
    const value = document.getElementById("medicine-search").value;
    if (value.trim()) onSearch(value);
  };

  return (
    <div className="search-section">
      <input
        id="medicine-search"
        placeholder="Search for medicines..."
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

export default SearchBar;
