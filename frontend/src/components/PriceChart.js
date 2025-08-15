import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
  Button,
  Menu
} from '@mui/material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  Analytics,
  PieChart as PieChartIcon,
  BarChart as BarChartIcon,
  ShowChart,
  ExpandMore
} from '@mui/icons-material';

const PriceChart = ({ prices }) => {
  const [chartType, setChartType] = useState('line');
  const [selectedCrypto, setSelectedCrypto] = useState('all');
  const [chartData, setChartData] = useState([]);
  const [anchorEl, setAnchorEl] = useState(null);

  useEffect(() => {
    if (prices && Object.keys(prices).length > 0) {
      const data = Object.entries(prices)
        .filter(([symbol, data]) => data && typeof data === 'object')
        .map(([symbol, data]) => ({
          symbol,
          price: Number(data.price_usd) || 0,
          change: Number(data.price_change_24h) || 0,
          volume: Number(data.volume_24h) || 0,
          marketCap: Number(data.market_cap) || 0
        }))
        .filter(item => item.price > 0); // Only include items with valid prices
      setChartData(data);
    } else {
      setChartData([]);
    }
  }, [prices]);

  const handleChartTypeClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleChartTypeClose = () => {
    setAnchorEl(null);
  };

  const handleChartTypeSelect = (type) => {
    setChartType(type);
    handleChartTypeClose();
  };

  const formatCurrency = (value) => {
    if (value === null || value === undefined || isNaN(value)) {
      return '$0.00';
    }
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(Number(value));
  };

  const formatPercentage = (value) => {
    if (value === null || value === undefined || isNaN(value)) {
      return '+0.00%';
    }
    return `${value >= 0 ? '+' : ''}${Number(value).toFixed(2)}%`;
  };

  const getCryptoColor = (symbol) => {
    const colors = {
      'BITCOIN': '#F7931A',
      'ETHEREUM': '#627EEA',
      'BINANCECOIN': '#F3BA2F',
      'SOLANA': '#14F195',
      'CARDANO': '#0033AD',
      'CHAINLINK': '#2A5ADA',
      'POLKADOT': '#E6007A',
      'LITECOIN': '#BFBBBB'
    };
    return colors[symbol] || '#2196F3';
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length && payload[0] && payload[0].payload) {
      const data = payload[0].payload;
      return (
        <Box
          sx={{
            bgcolor: 'rgba(0, 0, 0, 0.9)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: 2,
            p: 2,
            color: 'white'
          }}
        >
          <Typography variant="body2" fontWeight="bold">
            {data.symbol || 'Unknown'}
          </Typography>
          <Typography variant="body2">
            Price: {formatCurrency(payload[0].value)}
          </Typography>
          <Typography variant="body2">
            Change: {formatPercentage(data.change)}
          </Typography>
        </Box>
      );
    }
    return null;
  };

  const renderChart = () => {
    if (selectedCrypto === 'all') {
      // Show all cryptocurrencies
      switch (chartType) {
        case 'line':
          return (
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis 
                  dataKey="symbol" 
                  stroke="rgba(255,255,255,0.7)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="rgba(255,255,255,0.7)"
                  fontSize={12}
                  tickFormatter={(value) => formatCurrency(value)}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#2196F3" 
                  strokeWidth={3}
                  dot={{ fill: '#2196F3', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, stroke: '#2196F3', strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          );
        case 'area':
          return (
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis 
                  dataKey="symbol" 
                  stroke="rgba(255,255,255,0.7)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="rgba(255,255,255,0.7)"
                  fontSize={12}
                  tickFormatter={(value) => formatCurrency(value)}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#2196F3" 
                  fill="rgba(33, 150, 243, 0.3)"
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
          );
        case 'bar':
          return (
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis 
                  dataKey="symbol" 
                  stroke="rgba(255,255,255,0.7)"
                  fontSize={12}
                />
                <YAxis 
                  stroke="rgba(255,255,255,0.7)"
                  fontSize={12}
                  tickFormatter={(value) => formatCurrency(value)}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Bar 
                  dataKey="price" 
                  fill="#2196F3"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          );
        case 'pie':
          return (
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ symbol, price }) => `${symbol}: ${formatCurrency(price)}`}
                  outerRadius={120}
                  fill="#8884d8"
                  dataKey="price"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getCryptoColor(entry.symbol)} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          );
        default:
          return null;
      }
    } else {
      // Show single cryptocurrency
      const singleCryptoData = chartData.filter(item => item.symbol === selectedCrypto);
      if (singleCryptoData.length === 0) return null;

      const cryptoData = singleCryptoData[0];
      const data = [
        { name: 'Current', value: cryptoData.price || 0 },
        { name: '24h Change', value: Math.abs(cryptoData.change || 0) }
      ];

      return (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis 
              dataKey="name" 
              stroke="rgba(255,255,255,0.7)"
              fontSize={12}
            />
            <YAxis 
              stroke="rgba(255,255,255,0.7)"
              fontSize={12}
              tickFormatter={(value) => formatCurrency(value)}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke={getCryptoColor(selectedCrypto)} 
              strokeWidth={3}
              dot={{ fill: getCryptoColor(selectedCrypto), strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: getCryptoColor(selectedCrypto), strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      );
    }
  };

  const getMarketStats = () => {
    if (chartData.length === 0) {
      return {
        totalMarketCap: 0,
        totalVolume: 0,
        avgChange: 0,
        topPerformer: null
      };
    }
    
    const totalMarketCap = chartData.reduce((sum, item) => sum + (item.marketCap || 0), 0);
    const totalVolume = chartData.reduce((sum, item) => sum + (item.volume || 0), 0);
    const avgChange = chartData.reduce((sum, item) => sum + (item.change || 0), 0) / chartData.length;
    const topPerformer = chartData.reduce((max, item) => 
      (item.change || 0) > (max.change || 0) ? item : max, chartData[0]);

    return {
      totalMarketCap,
      totalVolume,
      avgChange,
      topPerformer
    };
  };

  const stats = getMarketStats();

  return (
    <Box>
      {/* Chart Controls */}
      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={4}>
        <Box display="flex" gap={3} alignItems="flex-start">
          <Box display="flex" flexDirection="column" alignItems="flex-start">
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mb: 1, fontWeight: 500 }}>
              Chart Type
            </Typography>
            <Button
              variant="outlined"
              onClick={handleChartTypeClick}
              endIcon={<ExpandMore />}
              sx={{
                borderColor: 'rgba(255,255,255,0.3)',
                color: 'white',
                minWidth: 160,
                height: 40,
                justifyContent: 'space-between',
                '&:hover': {
                  borderColor: 'rgba(255,255,255,0.5)',
                  bgcolor: 'rgba(255,255,255,0.1)'
                }
              }}
            >
              {chartType === 'line' && <ShowChart sx={{ mr: 1 }} />}
              {chartType === 'area' && <TrendingUp sx={{ mr: 1 }} />}
              {chartType === 'bar' && <BarChartIcon sx={{ mr: 1 }} />}
              {chartType === 'pie' && <PieChartIcon sx={{ mr: 1 }} />}
              {chartType.charAt(0).toUpperCase() + chartType.slice(1)} Chart
            </Button>
          </Box>
          
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleChartTypeClose}
            PaperProps={{
              sx: {
                bgcolor: 'rgba(0,0,0,0.9)',
                border: '1px solid rgba(255,255,255,0.2)',
                mt: 1
              }
            }}
          >
            <MenuItem onClick={() => handleChartTypeSelect('line')}>
              <ShowChart sx={{ mr: 1 }} />
              Line Chart
            </MenuItem>
            <MenuItem onClick={() => handleChartTypeSelect('area')}>
              <TrendingUp sx={{ mr: 1 }} />
              Area Chart
            </MenuItem>
            <MenuItem onClick={() => handleChartTypeSelect('bar')}>
              <BarChartIcon sx={{ mr: 1 }} />
              Bar Chart
            </MenuItem>
            <MenuItem onClick={() => handleChartTypeSelect('pie')}>
              <PieChartIcon sx={{ mr: 1 }} />
              Pie Chart
            </MenuItem>
          </Menu>

          <Box display="flex" flexDirection="column" alignItems="flex-start">
            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mb: 1, fontWeight: 500 }}>
              Cryptocurrency
            </Typography>
            <FormControl sx={{ minWidth: 200 }}>
              <Select
                value={selectedCrypto}
                onChange={(e) => setSelectedCrypto(e.target.value)}
                sx={{
                  color: 'white',
                  height: 40,
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'rgba(255,255,255,0.3)'
                  },
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'rgba(255,255,255,0.5)'
                  },
                  '& .MuiSvgIcon-root': {
                    color: 'rgba(255,255,255,0.7)'
                  }
                }}
              >
                <MenuItem value="all">All Cryptocurrencies</MenuItem>
                {Object.keys(prices || {}).map((symbol) => (
                  <MenuItem key={symbol} value={symbol}>
                    {symbol}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </Box>
      </Box>

      {/* Market Statistics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            bgcolor: 'rgba(76, 175, 80, 0.1)', 
            border: '1px solid rgba(76, 175, 80, 0.3)',
            borderRadius: 2,
            height: '100%',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 20px rgba(76, 175, 80, 0.2)'
            }
          }}>
            <CardContent sx={{ textAlign: 'center', p: 2 }}>
              <Typography variant="h6" color="#4CAF50" fontWeight="bold" sx={{ mb: 1 }}>
                Total Market Cap
              </Typography>
              <Typography variant="h5" color="white" fontWeight="bold">
                {formatCurrency(stats.totalMarketCap)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            bgcolor: 'rgba(33, 150, 243, 0.1)', 
            border: '1px solid rgba(33, 150, 243, 0.3)',
            borderRadius: 2,
            height: '100%',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 20px rgba(33, 150, 243, 0.2)'
            }
          }}>
            <CardContent sx={{ textAlign: 'center', p: 2 }}>
              <Typography variant="h6" color="#2196F3" fontWeight="bold" sx={{ mb: 1 }}>
                Total Volume (24h)
              </Typography>
              <Typography variant="h5" color="white" fontWeight="bold">
                {formatCurrency(stats.totalVolume)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            bgcolor: 'rgba(255, 152, 0, 0.1)', 
            border: '1px solid rgba(255, 152, 0, 0.3)',
            borderRadius: 2,
            height: '100%',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 20px rgba(255, 152, 0, 0.2)'
            }
          }}>
            <CardContent sx={{ textAlign: 'center', p: 2 }}>
              <Typography variant="h6" color="#FF9800" fontWeight="bold" sx={{ mb: 1 }}>
                Average Change
              </Typography>
              <Typography variant="h5" color="white" fontWeight="bold">
                {formatPercentage(stats.avgChange)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ 
            bgcolor: 'rgba(156, 39, 176, 0.1)', 
            border: '1px solid rgba(156, 39, 176, 0.3)',
            borderRadius: 2,
            height: '100%',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 20px rgba(156, 39, 176, 0.2)'
            }
          }}>
            <CardContent sx={{ textAlign: 'center', p: 2 }}>
              <Typography variant="h6" color="#9C27B0" fontWeight="bold" sx={{ mb: 1 }}>
                Top Performer
              </Typography>
              <Typography variant="h6" color="white" fontWeight="bold" sx={{ mb: 1 }}>
                {stats.topPerformer?.symbol || 'N/A'}
              </Typography>
              <Chip 
                label={formatPercentage(stats.topPerformer?.change || 0)}
                size="small"
                sx={{ 
                  bgcolor: '#9C27B0',
                  color: 'white',
                  fontWeight: 'bold'
                }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Chart */}
      <Card sx={{ 
        bgcolor: 'rgba(255,255,255,0.05)', 
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: 3,
        transition: 'all 0.3s ease',
        minHeight: 450,
        '&:hover': {
          boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
        }
      }}>
        <CardContent sx={{ p: 3, height: '100%' }}>
          {chartData.length > 0 ? (
            <Box sx={{ height: 400 }}>
              {renderChart()}
            </Box>
          ) : (
            <Box display="flex" justifyContent="center" alignItems="center" height={400}>
              <Typography variant="h6" color="rgba(255,255,255,0.7)">
                Loading chart data...
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default PriceChart; 