import React from 'react';
import {
    Drawer, List, ListItem, ListItemButton, ListItemIcon,
    ListItemText, Toolbar, Typography, Box, Divider
} from '@mui/material';
import {
    Assignment as OutpassIcon,
    Description as TemplateIcon,
    Logout as LogoutIcon,
    Dashboard as DashboardIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 260;

const Sidebar = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const menuItems = [
        { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
        { text: 'Outpass Requests', icon: <OutpassIcon />, path: '/dashboard' },
        { text: 'Template Editor', icon: <TemplateIcon />, path: '/templates' },
    ];

    const handleLogout = () => {
        localStorage.removeItem('adminToken');
        navigate('/');
    };

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: drawerWidth,
                    boxSizing: 'border-box',
                    backgroundColor: '#1e293b', // Deep Slate
                    color: '#f8fafc',
                },
            }}
        >
            <Toolbar sx={{ py: 3, px: 2 }}>
                <Box display="flex" alignItems="center" gap={1.5}>
                    <Box
                        sx={{
                            width: 35,
                            height: 35,
                            bgcolor: 'primary.main',
                            borderRadius: 1,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 'bold',
                            fontSize: '1.2rem'
                        }}
                    >
                        A
                    </Box>
                    <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: 0.5 }}>
                        ADMIN PORTAL
                    </Typography>
                </Box>
            </Toolbar>

            <Box sx={{ overflow: 'auto', mt: 2 }}>
                <List sx={{ px: 1.5 }}>
                    {menuItems.map((item) => (
                        <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
                            <ListItemButton
                                onClick={() => navigate(item.path)}
                                selected={location.pathname === item.path}
                                sx={{
                                    borderRadius: 1,
                                    '&.Mui-selected': {
                                        bgcolor: 'primary.main',
                                        '&:hover': { bgcolor: 'primary.dark' },
                                    },
                                    '&:hover': { bgcolor: 'rgba(255,255,255,0.05)' },
                                    transition: 'background-color 0.2s',
                                }}
                            >
                                <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText
                                    primary={item.text}
                                    primaryTypographyProps={{ fontWeight: 500, fontSize: '0.95rem' }}
                                />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </Box>

            <Box sx={{ mt: 'auto', p: 2 }}>
                <Divider sx={{ bgcolor: 'rgba(255,255,255,0.1)', mb: 2 }} />
                <ListItem disablePadding>
                    <ListItemButton
                        onClick={handleLogout}
                        sx={{
                            borderRadius: 1,
                            color: '#ef4444', // Red
                            '&:hover': { bgcolor: 'rgba(239, 68, 68, 0.1)' },
                        }}
                    >
                        <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>
                            <LogoutIcon />
                        </ListItemIcon>
                        <ListItemText primary="Logout" primaryTypographyProps={{ fontWeight: 500 }} />
                    </ListItemButton>
                </ListItem>
            </Box>
        </Drawer>
    );
};

export default Sidebar;
