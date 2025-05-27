# RAG Corpus Manager - Streamlit App

A modern, minimalist Streamlit application for managing RAG corpus documents with a clean, modular architecture.

## 🏗️ Architecture

The application is built with a modular structure for maintainability and scalability:

```
corpus_manager/
├── app.py                      # Main application entry point
├── config.py                   # Configuration and environment variables
├── components/                 # Reusable UI components
│   ├── header.py              # Main header component
│   ├── metrics.py             # Metrics cards component
│   ├── sidebar.py             # Sidebar controls component
│   └── styles.py              # CSS styling
├── pages/                     # Page-specific components
│   ├── document_list.py       # Document listing and management
│   ├── analytics.py           # Analytics and visualizations
│   └── bulk_operations.py     # Bulk operations interface
└── utils/                     # Utility modules
    ├── vertex_ai.py           # Vertex AI RAG operations
    └── formatters.py          # Data formatting utilities
```

## 🚀 Features

### 📋 Document Management
- **List Documents**: View all documents in your RAG corpus
- **Search & Filter**: Find documents by name or file type
- **Document Details**: View metadata and resource information
- **Individual Delete**: Remove single documents with confirmation

### 📊 Analytics Dashboard
- **File Type Distribution**: Visual breakdown of document types
- **Size Analytics**: Document size statistics and charts
- **Upload Timeline**: Track document uploads over time
- **Detailed Breakdowns**: Expandable detailed views

### 🔧 Bulk Operations
- **Multi-Select**: Choose multiple documents for batch operations
- **Select All**: Quick selection of entire corpus
- **Bulk Delete**: Remove multiple documents at once
- **Operation Summary**: Clear feedback on bulk operations

### 🎛️ Controls
- **Upload Documents**: Drag & drop file upload
- **Refresh Data**: Manual data refresh
- **Danger Zone**: Critical operations with safeguards

## 🎨 Design Philosophy

### Modern Minimalism
- Clean, uncluttered interface
- Consistent color palette and typography
- Intuitive navigation and workflows
- Responsive design for all screen sizes

### User Experience
- Clear visual hierarchy
- Contextual help and tooltips
- Immediate feedback for all actions
- Confirmation dialogs for destructive operations

### Performance
- Cached data operations
- Efficient component rendering
- Minimal re-renders and API calls

## 🛠️ Configuration

The app is configured through environment variables loaded from `.env`:

```bash
# Required Vertex AI Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
RAG_CORPUS_NAME=your-corpus-name

# Optional Configuration
EMBEDDING_MODEL=text-embedding-005
```

## 🔧 Customization

### Adding New Components
1. Create component in `components/` directory
2. Follow the naming convention: `component_name.py`
3. Export main function as `render_component_name()`
4. Import and use in `app.py`

### Adding New Pages
1. Create page in `pages/` directory
2. Follow the naming convention: `page_name.py`
3. Export main function as `render_page_name()`
4. Add tab in `app.py`

### Styling
- All CSS is centralized in `components/styles.py`
- Use CSS custom properties for consistent theming
- Follow the existing design system

### Utilities
- Add reusable functions to appropriate utility modules
- Use type hints for all functions
- Follow Python best practices

## 📱 Responsive Design

The app is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile devices

Key responsive features:
- Flexible grid layouts
- Scalable typography
- Touch-friendly interactions
- Optimized mobile navigation

## 🔒 Security

- Input validation for all user inputs
- Confirmation dialogs for destructive operations
- Secure file upload handling
- Environment variable configuration

## 🚀 Running the App

### Using the Launcher
```bash
# From the root directory
conda activate student-rag
source keys/service-account.env
streamlit run run_corpus_manager.py
```

### Direct Streamlit Command
```bash
# From the root directory
conda activate student-rag
source keys/service-account.env
streamlit run corpus_manager/app.py
```

### Custom Port
```bash
streamlit run run_corpus_manager.py --server.port 8502
```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 conventions
- Use type hints for all functions
- Write descriptive docstrings
- Keep functions focused and small

### Component Design
- Each component should have a single responsibility
- Use consistent parameter patterns
- Return structured data from components
- Handle errors gracefully

### State Management
- Use `st.session_state` for UI state
- Clear state appropriately on actions
- Avoid global state variables
- Cache expensive operations

## 🐛 Troubleshooting

### Common Issues

**App won't start**
- Check environment variables are set
- Verify Vertex AI authentication
- Ensure corpus exists

**Documents not loading**
- Check corpus resource name
- Verify API permissions
- Try refreshing the data

**Upload failures**
- Check file type restrictions
- Verify file size limits
- Ensure corpus write permissions

### Debug Mode
Enable debug mode by setting:
```bash
export DEBUG_MODE=true
```

## 🔄 Future Enhancements

Planned features:
- Document preview functionality
- Advanced search with filters
- Export/import capabilities
- User management and permissions
- API endpoint integration
- Real-time updates 